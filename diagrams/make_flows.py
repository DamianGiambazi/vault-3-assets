"""make_flows.py: the Vault 1, Vault 2 and vector-snake data-flow diagrams (1600x900 SVG), drawn in
the same visual system as V3-DIAGRAM-the-door.svg."""
from html import escape

W, H = 1600, 900
INK, MUTED, EDGE = "#1F2430", "#5B6472", "#8A94A6"
STYLE = {   # fill, stroke, stroke-width, title colour, text colour
    "file":    ("#FFFFFF", EDGE, 2, INK, MUTED),
    "tool":    ("#E3ECFA", "#2F5DA8", 2.5, INK, INK),
    "human":   ("#FFF4EE", "#B4532A", 2.5, INK, MUTED),
    "verdict": ("#1F2430", "#1F2430", 2, "#FFFFFF", "#D7DCE4"),
    "fail":    ("#FCEDED", "#B42A2A", 2, "#8E1F1F", "#8E1F1F"),
    "note":    ("#FFFFFF", EDGE, 1.5, INK, MUTED),
}
LEGEND = [("file", "files and evidence"), ("tool", "a tool runs"), ("human", "you decide or write first"),
          ("verdict", "a verdict word"), ("fail", "fails closed")]


class Svg:
    def __init__(self, title, subtitle, thesis=None):
        self.out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
                    'font-family="Segoe UI, Inter, Helvetica, Arial, sans-serif">',
                    f"<title>{escape(title)}: {escape(subtitle)}</title>",
                    '<defs>'
                    f'<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{MUTED}"/></marker>'
                    '<marker id="r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#B42A2A"/></marker>'
                    '<marker id="o" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#B4532A"/></marker>'
                    '</defs>',
                    f'<rect width="{W}" height="{H}" fill="#FAF8F4"/>',
                    f'<text x="60" y="62" font-size="32" font-weight="700" fill="{INK}">{escape(title)}</text>',
                    f'<text x="60" y="94" font-size="19" fill="{MUTED}">{escape(subtitle)}</text>']
        if thesis:
            for i, line in enumerate(thesis):
                self.out.append(f'<text x="{W-60}" y="{58 + 26*i}" text-anchor="end" font-size="19" '
                                f'font-style="italic" fill="{INK}">{escape(line)}</text>')

    def box(self, x, y, w, h, title, lines=(), kind="file", size=21, sub=15):
        fill, stroke, sw, tc, lc = STYLE[kind]
        self.out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        n = 1 + len(lines)
        block = size + (len(lines) * (sub + 6))
        top = y + (h - block) / 2 + size - 3
        cx = x + w / 2
        self.out.append(f'<text x="{cx}" y="{top:.0f}" text-anchor="middle" font-size="{size}" font-weight="700" fill="{tc}">{escape(title)}</text>')
        for i, ln in enumerate(lines):
            mono = ln.startswith("`") and ln.endswith("`")
            t = ln.strip("`")
            fam = ' font-family="Cascadia Mono, Consolas, Menlo, monospace"' if mono else ""
            self.out.append(f'<text x="{cx}" y="{top + 8 + (i+1)*(sub+6):.0f}" text-anchor="middle" font-size="{sub - (1 if mono else 0)}"{fam} fill="{lc}">{escape(t)}</text>')

    def arrow(self, pts, colour="grey", dashed=False, both=False):
        stroke, m = {"grey": (MUTED, "a"), "red": ("#B42A2A", "r"), "orange": ("#B4532A", "o")}[colour]
        d = "M" + " L".join(f"{x} {y}" for x, y in pts)
        extra = ' stroke-dasharray="7 6"' if dashed else ""
        start = f' marker-start="url(#{m})"' if both else ""
        self.out.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="2.5"{extra}{start} marker-end="url(#{m})"/>')

    def label(self, x, y, text, anchor="middle", colour=MUTED, size=15, bold=False):
        self.out.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}"{" font-weight=\"600\"" if bold else ""} fill="{colour}">{escape(text)}</text>')

    def band(self, x, y, w, h, text, right=False):
        self.out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#EEF2F7" stroke="{EDGE}" stroke-width="1.5" stroke-dasharray="9 7"/>')
        self.out.append(f'<text x="{x+w-18 if right else x+18}" y="{y+24}" text-anchor="{"end" if right else "start"}" font-size="14" font-weight="600" letter-spacing="1" fill="{MUTED}">{escape(text)}</text>')

    def legend(self, y=H - 34):
        x = 60
        for kind, text in LEGEND:
            fill, stroke, sw, *_ = STYLE[kind]
            self.out.append(f'<rect x="{x}" y="{y-13}" width="22" height="16" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
            self.label(x + 30, y, text, anchor="start", size=14)
            x += 40 + len(text) * 7.6

    def save(self, path):
        self.out.append("</svg>")
        open(path, "w", encoding="utf-8").write("\n".join(self.out))


# ---------------------------------------------------------------------------------------------------
# VAULT 1: documents in, one cited answer out (the capstone pipeline)
# ---------------------------------------------------------------------------------------------------
s = Svg("Vault 1 · The 100% Rule: data flow",
        "Documents in, one cited answer out. Each step is checked before the next one may run.",
        ["Write the answer down", "before you run it."])
X = [60, 450, 840, 1230]; BW = 310
R1, R2, R3, BH = 150, 400, 620, 130
# row 1: left -> right
s.box(X[0], R1, BW, BH, "input\\", ["your .txt documents", "+ question.txt (one sentence,", "worded unlike the text)"])
s.box(X[1], R1, BW, BH, "vector-snake 2.0", ["cuts each file into passages", "turns each into 384 numbers", "question in the SAME run"], "tool")
s.box(X[2], R1, BW, BH, "vectors\\", ["*_vectors.csv: text + numbers", "*_manifest.json: one per file", "*_run_manifest.json: the run"])
s.box(X[3], R1, BW, BH, "Hugging Face cache", ["all-MiniLM-L6-v2", "the translator, used offline", "hf CLI 2.2.0 shows what's there"])
s.arrow([(X[0]+BW, R1+65), (X[1]-8, R1+65)])
s.arrow([(X[1]+BW, R1+65), (X[2]-8, R1+65)])
s.arrow([(X[3]+BW/2, R1+BH), (X[3]+BW/2, R1+BH+40), (X[1]+BW/2+60, R1+BH+40), (X[1]+BW/2+60, R1+BH+8)], dashed=True)
s.label(X[3]+BW/2-20, R1+BH+62, "the model, read from disk (--offline)", anchor="end")
# row 2: right -> left
s.box(X[2], R2, BW, BH, "DuckDB · audit.sql", ["the gate: 1 run · 0 failed", "1 model · 1 size · 1 question", "`AUDIT_PASS  EXPORT_OK`"], "tool")
s.box(X[1], R2, BW, BH, "corpus.parquet", ["+ question.parquet", "clean evidence, typed vectors", "written only if the gate passed"])
s.box(X[3], R2, BW, BH, "AUDIT_FAIL", ["e.g. runs=2 or question_rows=2", "nothing is exported:", "the next step can't run"], "fail")
s.box(X[0], R2, BW, BH, "The 100% Rule", ["“Are you 100% ready to execute", "the prompt, or do you need", "more information?”"], "human")
s.arrow([(X[2]+BW/2, R1+BH), (X[2]+BW/2, R2-8)])
s.arrow([(X[2], R2+65), (X[1]+BW+8, R2+65)])
s.arrow([(X[2]+BW, R2+65), (X[3]-8, R2+65)], "red")
s.label((X[2]+BW+X[3])/2, R2+55, "fail", colour="#B42A2A")
# row 3: left -> right (capstone_rag.py)
s.band(X[0]-20, R3-38, 3*BW + 2*80 + 40, BH+56, "capstone_rag.py · Vault 1's smoke-lab venv", right=True)
s.box(X[0], R3, BW, BH, "LanceDB 0.40.0", ["question vs every passage", "3 closest passages", "(temp table, deleted after)"], "tool")
s.box(X[1], R3, BW, BH, "Ollama", ["smollm2:360m-instruct-q8_0", "reads only those 3 passages", "`{answer, source_id}`"], "tool")
s.box(X[2], R3, BW, BH, "4 checks", ["schema · citation", "grounding · canary", "(the cited passage holds the fact)"], "tool")
s.box(X[3], R3, BW, BH, "CAPSTONE_OK", ["answer: “15 years”", "cites notes_0652_0001", "~50 s on SPOOKY"], "verdict")
s.arrow([(X[1]+BW/2, R2+BH), (X[1]+BW/2, R2+BH+38), (X[0]+BW/2, R2+BH+38), (X[0]+BW/2, R3-8)])
s.arrow([(X[0]+BW, R3+65), (X[1]-8, R3+65)])
s.arrow([(X[1]+BW, R3+65), (X[2]-8, R3+65)])
s.arrow([(X[2]+BW, R3+65), (X[3]-8, R3+65)])
# the prediction feeds the checks
s.box(X[2], R3+BH+28, BW, 62, "CAPSTONE_CANARY", ["written BEFORE the run: the expected fact"], "human", size=17, sub=14)
s.arrow([(X[2]+BW/2, R3+BH+28), (X[2]+BW/2, R3+BH+8)], "orange")
s.legend(); s.save("/home/claude/v3-cards/V1-FLOW-the-100-percent-rule.svg")

# ---------------------------------------------------------------------------------------------------
# VAULT 2: find the spine, seal it, declare it, make it travel
# ---------------------------------------------------------------------------------------------------
s = Svg("Vault 2 · The SSOT Library: data flow",
        "Find the spine by meaning, seal the prediction first, declare the truth, then make it travel.",
        ["The machine proposes;", "the author declares."])
X = [40, 352, 664, 976, 1288]; BW = 272; BH = 112
R = [138, 312, 486, 660]
# row 1: seal and translate (left -> right)
s.box(X[0], R[0], BW, BH, "book\\ + spine\\", ["24 chapters + 4 questions", "PREDICTION.md written first", "(no content word shared)"], "human")
s.box(X[1], R[0], BW, BH, "git commit: the seal", ["git as notary", "`13913f5  16:02:34Z`", "before any run"], "tool")
s.box(X[2], R[0], BW, BH, "vector-snake --dry-run", ["cuts only, no numbers", "28 files \u2192 33 passages", "every cut on a paragraph break"], "tool")
s.box(X[3], R[0], BW, BH, "vector-snake (real run)", ["--max-chars 800 --offline", "`20261101_171405`", "`passed=28 warned=0`"], "tool")
s.box(X[4], R[0], BW, BH, "receipts\\", ["28 × vectors.csv (ignored by git)", "28 × manifest.json", "1 × run_manifest.json"])
for i in range(4):
    s.arrow([(X[i]+BW, R[0]+56), (X[i+1]-8, R[0]+56)])
# row 2: gate and search (right -> left)
s.box(X[4], R[1], BW, BH, "DuckDB · gate.sql", ["1 run · 1 model · 24 chapters", "nothing truncated", "`GATE_PASS  chunks=29`"], "tool")
s.box(X[3], R[1], BW, BH, "corpus.parquet", ["29 passages", "+ questions.parquet (4)", "same translator, same run"])
s.box(X[2], R[1], BW, BH, "spine_search.py", ["LanceDB · cosine distance", "a chapter scores", "its closest passage"], "tool")
s.box(X[1], R[1], BW, BH, "SPINE_PARTIAL 1/4", ["the watcher: 1, 7, 24, 19 ✔", "the lie, the cost, the door ✘", "keyword 'window': 9 chapters"], "verdict")
s.box(X[0], R[1], BW, BH, "seal-check.ps1", ["seal 16:02:34Z", "run 16:14:05Z", "`SEALED_BEFORE_RUN`"], "tool")
s.arrow([(X[4]+BW/2, R[0]+BH), (X[4]+BW/2, R[1]-8)])
for i in range(4, 0, -1):
    s.arrow([(X[i], R[1]+56), (X[i-1]+BW+8, R[1]+56)])
s.arrow([(X[1]+BW/2-40, R[0]+BH), (X[1]+BW/2-40, R[0]+BH+30), (X[0]+BW/2, R[0]+BH+30), (X[0]+BW/2, R[1]-8)], dashed=True)
s.label(X[0]+BW/2+12, R[0]+BH+24, "the commit time", anchor="start", size=14)
# row 3: declare and travel (left -> right)
s.box(X[0], R[2], BW, BH, "The author declares", ["SSOT.md + CONSTITUTION.md", "the evidence, labelled as such", "“similarity is not significance”"], "human")
s.box(X[1], R[2], BW, BH, "git commit", ["SSOT + Constitution", "+ 29 run receipts, no vectors", "`131ee69  lock the spine`"], "tool")
s.box(X[2], R[2], BW, BH, "GitHub · novel-ssot", ["first push, Public", "git commits, GitHub carries", "receipts in, vectors out"], "tool")
s.box(X[3], R[2], BW, BH, "web edit → git pull", ["Chapter 2 note, from the phone", "`74fd9a4  Fast-forward`", "SSOT.md | 1 +"], "human")
s.box(X[4], R[2], BW, BH, "HANDOVER.md", ["+ spine\\INHERITANCE.md", "dc9e692, HEAD today", "what the next session needs"])
s.arrow([(X[0]+BW/2, R[1]+BH), (X[0]+BW/2, R[2]-8)])
for i in range(4):
    s.arrow([(X[i]+BW, R[2]+56), (X[i+1]-8, R[2]+56)])
# row 4: rebuild anywhere (left -> right) + reload check
s.box(X[0], R[3], BW, BH, "git clone", ["a fresh copy from GitHub", "29 receipts, no vectors", "novel-ssot-clone"], "tool")
s.box(X[1], R[3], BW, BH, "vector-snake rebuild", ["same book, same settings", "same model snapshot", "`passed=28`"], "tool")
s.box(X[2], R[3], BW, BH, "DuckDB · compare.sql", ["cuts: text hashes + spans", "numbers: min cosine", "receipts vs rebuild"], "tool")
s.box(X[3], R[3], BW, BH, "REBUILD_MATCHES_RECEIPT", ["`CUTS_IDENTICAL  33`", "`VECTORS_MATCH  1.0`", "truth with a recipe travels"], "verdict", size=18)
s.box(X[4], R[3], BW, BH, "The reload check", ["a fresh chat, no memory", "reads 4 files and says", "what it doesn't know"], "human")
s.arrow([(X[2]+BW/2, R[2]+BH), (X[2]+BW/2, R[2]+BH+30), (X[0]+BW/2, R[2]+BH+30), (X[0]+BW/2, R[3]-8)])
for i in range(3):
    s.arrow([(X[i]+BW, R[3]+56), (X[i+1]-8, R[3]+56)])
s.arrow([(X[4]+BW/2, R[2]+BH), (X[4]+BW/2, R[3]-8)])
s.label(X[4]+BW/2+10, R[2]+BH+36, "short video", anchor="start", size=14)
s.legend(); s.save("/home/claude/v3-cards/V2-FLOW-the-ssot-library.svg")

# ---------------------------------------------------------------------------------------------------
# VECTOR-SNAKE 2.0: one run, inside
# ---------------------------------------------------------------------------------------------------
s = Svg("vector-snake 2.0 · inside one run",
        "Local only. Cut by structure, translate by meaning, audit everything, fail closed.",
        ["We cut by structure.", "We search by meaning."])
X = [40, 352, 664, 976, 1288]; BW = 272; BH = 118
R = [140, 330, 520, 710]
# row 1: read and cut (left -> right)
s.box(X[0], R[0], BW, BH, "input folder", [".txt and .md in the vaults", "also docx, pdf, html, csv,", "json, eml… (own extractors)"])
s.box(X[1], R[0], BW, BH, "extract + decode", ["text out of each format", "encoding detected", "source sha256 recorded"], "tool")
s.box(X[2], R[0], BW, BH, "normalize", ["line endings → \\n", "NBSP → space · Unicode NFC", "(--join-hard-wraps: opt-in)"], "tool")
s.box(X[3], R[0], BW, BH, "atomize (recursive)", ["paragraph → line → sentence", "→ word → character", "only where a piece is too big"], "tool")
s.box(X[4], R[0], BW, BH, "pack", ["atoms joined up to --max-chars", "(1000 default · 800 in Vault 2)", "pieces < 40 chars merged"], "tool")
for i in range(4):
    s.arrow([(X[i]+BW, R[0]+59), (X[i+1]-8, R[0]+59)])
# row 2: spans, audit, branch (right -> left)
s.box(X[4], R[1], BW, BH, "base spans", ["tile the text EXACTLY:", "no gap, no overlap,", "nothing lost or changed"], "tool")
s.box(X[3], R[1], BW, BH, "run-up (overlap)", ["≤ 120 chars, ≤ max_chars ÷ 3", "starts at a sentence, else a word", "a tracked prefix, never a rewrite"], "tool")
s.box(X[2], R[1], BW, BH, "structure audit", ["coverage_exact · spans_contiguous", "min / max size", "deterministic: same cuts every run"], "tool")
s.box(X[1], R[1], BW, BH, "--dry-run stops here", ["`*_preview.json`", "cuts + spans + run-ups", "no model, no numbers"], "note")
s.box(X[0], R[1], BW, BH, "a failed audit", ["no CSV is written", "the file is marked FAILED", "exit code 2 or 3"], "fail")
s.arrow([(X[4]+BW/2, R[0]+BH), (X[4]+BW/2, R[1]-8)])
s.arrow([(X[4], R[1]+59), (X[3]+BW+8, R[1]+59)])
s.arrow([(X[3], R[1]+59), (X[2]+BW+8, R[1]+59)])
s.arrow([(X[2], R[1]+59), (X[1]+BW+8, R[1]+59)], dashed=True)
s.arrow([(X[2]+40, R[1]+BH), (X[2]+40, R[1]+BH+34), (X[0]+BW/2, R[1]+BH+34), (X[0]+BW/2, R[1]+BH+8)], "red")
s.label(X[1]+BW/2, R[1]+BH+27, "fail", colour="#B42A2A")
# row 3: translate and check (left -> right... starts under the audit)
s.box(X[2], R[2], BW, BH, "embed", ["all-MiniLM-L6-v2 (local)", "384 numbers per passage", "normalized · --offline"], "tool")
s.box(X[3], R[2], BW, BH, "token telemetry", ["the model reads 256 tokens", "a longer passage is truncated", "→ WARN (Vault 2's gate refuses it)"], "tool")
s.box(X[4], R[2], BW, BH, "vector audit", ["one vector per passage", "384 numbers each", "no NaN, no infinity"], "tool")
s.arrow([(X[2]+BW/2+60, R[1]+BH), (X[2]+BW/2+60, R[2]-8)])
s.label(X[2]+BW/2+70, R[1]+BH+56, "pass", anchor="start", colour=INK, bold=True)
s.arrow([(X[2]+BW, R[2]+59), (X[3]-8, R[2]+59)])
s.arrow([(X[3]+BW, R[2]+59), (X[4]-8, R[2]+59)])
s.box(X[0], R[2], BW+BW//2+30, BH, "The 256-token window", ["checked, not cut by: cuts follow", "structure, then telemetry warns", "if a passage is too long to read"], "note", size=19)
# row 4: write (right -> left)
s.box(X[4], R[3], BW, BH, "*_vectors.csv", ["id · source_file · chunk_index", "created_utc · embedding_model", "vector_dim · text · vector_json"])
s.box(X[3], R[3], BW, BH, "round-trip audit", ["written atomically,", "then read back:", "rows and dims must match"], "tool")
s.box(X[2], R[3], BW, BH, "*_manifest.json", ["one per file: hashes, spans,", "run-ups, every check, telemetry", "the receipt Vault 2 commits"])
s.box(X[1], R[3], BW, BH, "*_run_manifest.json", ["run_id · config", "passed / warned / failed", "what the gates read first"])
s.box(X[0], R[3], BW, BH, "[SUMMARY]", ["`passed=28 warned=0 failed=0`", "exit 0 = all passed", "Vault 2, run 20261101_171405"], "verdict")
s.arrow([(X[4]+BW/2, R[2]+BH), (X[4]+BW/2, R[3]-8)])
for i in range(4, 0, -1):
    s.arrow([(X[i], R[3]+59), (X[i-1]+BW+8, R[3]+59)])
s.legend(); s.save("/home/claude/v3-cards/VS-FLOW-vector-snake.svg")
print("ok")
