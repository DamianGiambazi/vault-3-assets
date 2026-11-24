"""novel-door — the laptop's library, opened to any MCP client (Vault 3, build 1.1.4).

The laptop finds WHERE things are in the novel (meaning search over the Vault 2 index, keyword
search, chapter text). A client model works out WHAT they mean. One tool, behind a GitHub sign-in
handled by Arcade, lets the model PROPOSE an SSOT amendment as an issue on the novel's repo.
The author declares.

Rules this file enforces:
  - Text only crosses the boundary. No tool ever returns a vector.
  - The model sees the 24 chapters and nothing else: no SSOT, no prediction, no evidence table.
  - The door opens one room: issues on NOVEL_REPO only.
  - Every call is logged (calls.jsonl), so DuckDB can audit what left the machine.

Run (stdio, the transport MCP clients launch):  .venv\\Scripts\\python.exe server.py
Settings come from the environment (Claude Desktop's config "env" block), never from this file:
  NOVEL_SSOT             the working copy holding book\\ and spine\\*.parquet   (C:\\Dev\\novel-ssot)
  NOVEL_REPO             the only GitHub repository the door may write to     (DamianGiambazi/novel-ssot)
  NOVEL_GITHUB_PROVIDER  the Arcade auth-provider ID of your own GitHub App   (empty = Arcade's default)
  NOVEL_DOOR_LOG         the call log                                        (calls.jsonl next to this file)
  NOVEL_DOOR_SMOKE       "1" only inside mcp_smoke.py: the door never posts
"""
import atexit, json, os, re, shutil, sys, tempfile, time
from pathlib import Path
_T0 = time.perf_counter()

# 1.1.2 (V3 live, 3 Nov): MCP speaks UTF-8. On Windows a pipe defaults to the ANSI code page (cp1252), so a
# passage with an em dash went out as byte 0x97 and the client could not read it. Arcade's stdio transport
# reads sys.stdin and writes sys.stdout, so both are switched to UTF-8 before anything is read or written.
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from typing import Annotated

os.environ.setdefault("HF_HUB_OFFLINE", "1")          # the model is cached; never download
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

# 1.1.1 (V3 live, 3 Nov): torch and sentence-transformers are imported FIRST, in the main thread, before
# LanceDB or Arcade start any threads. 1.1.0 loaded them in a background thread; on Windows that thread
# could deadlock against the first client request (stuck at 337 MB, CPU flat, no reply).
from sentence_transformers import SentenceTransformer

def _note(msg: str) -> None:                          # stderr only: shows in Claude Desktop's MCP log
    print(f"novel_door: {msg} ({time.perf_counter() - _T0:.1f} s)", file=sys.stderr, flush=True)
_note("torch + sentence-transformers imported")

import httpx
import pyarrow as pa
import pyarrow.parquet as pq
import lancedb
from arcade_mcp_server import Context, MCPApp
from arcade_mcp_server.auth import GitHub

# ---- configuration (frozen at the final rehearsal) ---------------------------------------------
HERE      = Path(__file__).resolve().parent
BOOK      = Path(os.environ.get("NOVEL_SSOT", r"C:\Dev\novel-ssot"))
BOOK_REPO = os.environ.get("NOVEL_REPO", "DamianGiambazi/novel-ssot")
PROVIDER  = os.environ.get("NOVEL_GITHUB_PROVIDER", "").strip() or None
LOG       = Path(os.environ.get("NOVEL_DOOR_LOG", str(HERE / "calls.jsonl")))
SMOKE     = os.environ.get("NOVEL_DOOR_SMOKE") == "1"
MODEL     = "all-MiniLM-L6-v2"                        # same translator as the Vault 2 run
DIM       = 384
# -------------------------------------------------------------------------------------------------

def _fixed(t: pa.Table) -> pa.Table:
    """Parquet stores DuckDB's FLOAT[384] as a variable list; LanceDB wants a fixed-size vector."""
    flat = t.column("vector").combine_chunks().flatten()
    return t.set_column(t.schema.get_field_index("vector"), "vector",
                        pa.FixedSizeListArray.from_arrays(flat, DIM))

_corpus = _fixed(pq.read_table(BOOK / "spine" / "corpus.parquet"))      # written by Vault 2's gate.sql
# 1.1.3 (V3 live, 3 Nov): Claude Desktop may start TWO copies of the server at once (chat, and Cowork/Code).
# Each copy now builds its own private index in TEMP, so they never overwrite each other's table.
_INDEX = Path(tempfile.mkdtemp(prefix="novel_door_index_"))
atexit.register(shutil.rmtree, _INDEX, ignore_errors=True)
_table = lancedb.connect(str(_INDEX)).create_table("book", data=_corpus, mode="overwrite")
_note(f"index ready: {_corpus.num_rows} passages")

# The model loads now, before the server answers anyone: startup is slower, every search is fast.
_model = SentenceTransformer(MODEL, device="cpu")
_note("model loaded; ready for a client")

def _embed(text: str) -> list[float]:
    return _model.encode([text], normalize_embeddings=True)[0].tolist()

def _chapter_file(n: int) -> Path:
    return BOOK / "book" / "corpus" / f"ch-{n:02d}.md"

def _log(tool: str, args: dict, chapters: list[int], reply: dict) -> None:
    out = json.dumps(reply, ensure_ascii=False)
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "tool": tool, "args": args,
           "chapters": sorted(set(chapters)), "chars_out": len(out),
           "vector_in_output": '"vector"' in out}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

app = MCPApp(name="novel_door", version="1.1.4",
             instructions="A 24-chapter novel in draft notes. Search it by meaning or by keyword, read "
                          "chapters, and propose SSOT amendments as GitHub issues. You cannot edit the book.")

@app.tool
def search_by_meaning(
    question: Annotated[str, "A question or description, in your own words"],
    chapters: Annotated[int, "How many chapters to return (1-8)"] = 4,
) -> dict:
    """Find the chapters whose passages are closest in MEANING to the question (cosine distance,
    all-MiniLM-L6-v2). A chapter scores its closest passage. Returns passage text, never vectors."""
    k = max(1, min(int(chapters), 8))
    hits = _table.search(_embed(question)).distance_type("cosine").limit(_corpus.num_rows).to_list()
    best = {}
    for h in hits:                                     # nearest first: keep each chapter's best passage
        best.setdefault(h["chapter"], h)
    results = [{"chapter": int(h["chapter"]), "distance": round(h["_distance"], 4), "passage": h["text"]}
               for h in list(best.values())[:k]]
    out = {"question": question, "results": results}
    _log("search_by_meaning", {"question": question, "chapters": k}, [r["chapter"] for r in results], out)
    return out

@app.tool
def keyword_search(word: Annotated[str, "A word or short phrase (case-insensitive)"]) -> dict:
    """Find the chapters that literally contain a word. Fast, exact, and blind to meaning."""
    pat = re.compile(re.escape(word), re.IGNORECASE)
    results = []
    for n in range(1, 25):
        lines = [ln for ln in _chapter_file(n).read_text(encoding="utf-8").splitlines() if pat.search(ln)]
        if lines:
            results.append({"chapter": n, "hits": len(lines), "passage": lines[0]})
    out = {"word": word, "results": results}
    _log("keyword_search", {"word": word}, [r["chapter"] for r in results], out)
    return out

@app.tool
def read_chapter(chapter: Annotated[int, "Chapter number, 1-24"]) -> dict:
    """Return the full notes of one chapter."""
    n = int(chapter)
    if not 1 <= n <= 24:
        raise ValueError("chapter must be between 1 and 24")
    out = {"chapter": n, "text": _chapter_file(n).read_text(encoding="utf-8")}
    _log("read_chapter", {"chapter": n}, [n], out)
    return out

@app.tool(requires_auth=GitHub(id=PROVIDER))
async def propose_ssot_amendment(
    context: Context,
    title: Annotated[str, "One line: what should change in the SSOT"],
    proposal: Annotated[str, "The proposed wording and why, citing chapters"],
    evidence_chapters: Annotated[list[int], "Chapters that support the proposal"],
) -> dict:
    """Open a GitHub issue on the novel's repository proposing a change to SSOT.md.
    This does NOT change the SSOT: only the author can. Requires the author's GitHub sign-in."""
    token = context.get_auth_token_or_empty()
    if not token:
        raise ValueError("No GitHub authorization in context")
    if SMOKE:                                          # mcp_smoke.py: the door is open; read, never post
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(f"https://api.github.com/repos/{BOOK_REPO}",
                                 headers={"Authorization": f"Bearer {token}",
                                          "Accept": "application/vnd.github+json"})
        return {"smoke": True, "repo": BOOK_REPO, "repo_status": r.status_code,
                "door": "OPEN: a GitHub sign-in already exists. No issue was created."}
    body = (f"{proposal}\n\n**Evidence:** chapters {', '.join(str(c) for c in evidence_chapters)}\n\n"
            "---\n*Proposed by an AI client through the `novel_door` MCP server. "
            "This is a proposal, not a decision. The SSOT changes only when the author declares it.*")
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"https://api.github.com/repos/{BOOK_REPO}/issues",
                              headers={"Authorization": f"Bearer {token}",
                                       "Accept": "application/vnd.github+json",
                                       "X-GitHub-Api-Version": "2022-11-28"},
                              json={"title": f"[SSOT proposal] {title}", "body": body})
        if r.status_code >= 400:                       # 1.1.4: say exactly why GitHub refused
            try:
                msg = r.json().get("message", "")
            except ValueError:
                msg = r.text[:200]
            raise ValueError(
                f"GitHub refused: HTTP {r.status_code} on {BOOK_REPO}: {msg} | "
                f"needs: {r.headers.get('X-Accepted-GitHub-Permissions', '?')} | "
                f"token type: {'GitHub App user token' if token.startswith('ghu_') else token[:4] + '...'}")
        issue = r.json()
    out = {"issue": issue["number"], "url": issue["html_url"], "title": issue["title"]}
    _log("propose_ssot_amendment", {"title": title, "evidence_chapters": evidence_chapters},
         list(evidence_chapters), out)
    return out

if __name__ == "__main__":
    app.run()
