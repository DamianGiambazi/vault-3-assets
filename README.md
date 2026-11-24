# Vault 3 — The Door: Reference

Nov 4, 2026 · @Damian

## What Vault 3 is

Vault 3 opens the Vault 2 library to an outside reader. The laptop keeps the novel and serves it through a small MCP server; a frontier model in Claude Desktop reads it; one tool, behind the author's GitHub sign-in, lets the model propose an SSOT change as an issue. The author still decides, by commit. Every step is proved on the same 8 GB laptop as Vaults 1 and 2.

> **Draft status (4 Nov 2026):** the results below come from the rehearsal on SPOOKY, 3 Nov. They are checked against the recorded performance before this Reference is published.

The method carries beyond novels: keep your material local, serve it as text through a door you can audit, let a stronger reader do the reading, and keep the decision with a person.

- **Laptop** — Lenovo V15-IGL ("SPOOKY"): Intel Celeron N4020, 2 cores, 8 GB RAM, no AVX, Windows 11 Pro 25H2
- **Stack (from Vaults 1–2)** — DuckDB 1.5.6 · LanceDB 0.40.0 · all-MiniLM-L6-v2 (384 numbers; snapshot `1110a243...`) · PowerShell 7.6.9 · git 2.50.1 · the Vault 2 index (run `20261101_171405`, 29 passages)
- **New this vault** — Claude Desktop · Arcade CLI 1.17.1 · a project venv (`arcade-mcp-server` 1.33.0, `sentence-transformers` 6.1.0, `torch` 2.14.1) · the GitHub App `novel-door-damian` · the Arcade key `novel-door-github`
- **Corpus** — the same 24 chapters and 4 sealed questions as Vault 2
- **Videos** — *The Door: Your Laptop as a Library, Any AI as the Reader*: Part One the performance, Part Two the deep dive into how it was built

## The library, the reader and the door

Vault 2 ended at one of four: the laptop found the image (the watcher) and missed the meaning (the lie, the cost, the door). The answer is a better division of labour, not a bigger laptop.

The thesis: **"The laptop serves. The model reads. The author declares."** It was "the laptop finds" until the rehearsal: the reader read all 24 chapters and never used the search (see The proof).

**The statement in the novel's own words.** The protagonist's arc is "from the window to the door". The stack has been the figure in the window, watching. Now it has a door, and it still doesn't choose where to go.

| Who | Job | Built from |
| --- | --- | --- |
| The laptop (the library) | keeps the book; serves it through four tools; text out, never vectors; logs every call | Vault 1's stack, Vault 2's index |
| `novel_door` (the door) | speaks MCP, the protocol any AI client understands | Arcade's `arcade-mcp-server`, on the laptop |
| Claude Desktop (the reader) | reads the text and decides what it means | a frontier model, in the cloud |
| Arcade (the key-holder) | runs the GitHub sign-in; the token reaches the tool, never the model | an Arcade account and `arcade login` |
| GitHub (the record) | holds the proposal as an issue | Vault 2's public `novel-ssot` |
| The author | accepts or rejects; only a commit changes the SSOT | you |

The reader gets text through one plug; the only thing that leaves for GitHub is a proposal, and only after the author's sign-in.

## MCP and Arcade

MCP (the Model Context Protocol) is a standard plug between an AI client and a tool: any client that speaks it can use any server that speaks it. Here the client is Claude Desktop and the server is `novel_door`, a Python program on the laptop. They talk over stdio: Claude Desktop starts the program itself and exchanges plain JSON messages through its input and output. Nothing listens on the network.

Arcade does two jobs:

- **the framework:** `arcade-mcp-server` turns ordinary Python functions into MCP tools (`@app.tool`);
- **the key-holder:** a tool marked `requires_auth=GitHub(...)` gets a GitHub token from Arcade at the moment it runs. The first time, the tool returns a sign-in link instead; the author approves in a browser. The model only passes the link on; it never sees the token.

*the Vault 3 architecture · 6 parts, 1 door*

**Proposing is not deciding.** The one tool that acts opens a GitHub issue, never a commit or a pull request:

| On GitHub | What it is | Changes the files? | Who does it here |
| --- | --- | --- | --- |
| Commit | a saved change to the files | yes | only the author |
| Pull request | a proposed change, waiting to be merged | not until merged | nobody |
| Issue | a note on the project: a question, a bug, a proposal | no | the AI, through the door |

The author answers an issue with a commit whose message says `closes #n`: the issue and the commit then point at each other, so the record shows who suggested and who decided. It is Vault 2's rule, the machine proposes, the author declares, built into the workflow.

## The server: novel_door

`server.py`, build 1.1.4, is one file of about 190 lines. It loads the Vault 2 index, builds a LanceDB table and exposes four tools. Claude Desktop sees them under these names:

| Tool | Sign-in | Returns |
| --- | --- | --- |
| `NovelDoor_SearchByMeaning` | no | the closest chapters (a chapter scores its closest passage, as in Vault 2), their cosine distance and passage text |
| `NovelDoor_KeywordSearch` | no | the chapters containing a word, with the first matching line |
| `NovelDoor_ReadChapter` | no | the notes of one chapter, 1–24 |
| `NovelDoor_ProposeSsotAmendment` | GitHub, through Arcade | an issue number and link on the one configured repository |

Four rules the file enforces:

1. **Text only crosses the boundary.** No tool returns a vector.
2. **The model sees the 24 chapters and nothing else**: not `SSOT.md`, not the predictions, not the Machine Evidence table.
3. **The door opens one room**: issues on `NOVEL_REPO` only, with the footer "This is a proposal, not a decision."
4. **Every call is logged** to `calls.jsonl` (time, tool, what was asked, chapters, characters out, a flag for any vector), so DuckDB can audit what left the laptop.

Settings come from the environment, never from the file: `NOVEL_SSOT` (the book), `NOVEL_REPO` (the one repository), `NOVEL_GITHUB_PROVIDER` (the Arcade key's name), plus `ARCADE_USAGE_TRACKING=0` and `HF_HUB_OFFLINE=1`.

Three Windows fixes, found in rehearsal and kept in the code:

| Build | Fix | Because |
| --- | --- | --- |
| 1.1.1 | torch and MiniLM load first, in the main thread | loading in a background thread deadlocked against the first request |
| 1.1.2 | stdin and stdout switched to UTF-8 | a Windows pipe defaults to cp1252, so an em dash crashed the client |
| 1.1.3 | a private index per copy, in TEMP; startup notes in the log | Claude Desktop starts two copies at once |

Build 1.1.4 adds GitHub's exact reason when it refuses a write. Startup takes 40–80 s on SPOOKY; every search after that takes about 0.2 s.

## The workshop: three installs and one key

Everything the door needs was built once, in the rehearsal, and stays. The performance shows it already built.

| Part | What | Check |
| --- | --- | --- |
| The reader | Claude Desktop (memory off, past chats off) | Settings → Extensions: `novel_door` Running |
| The CLI | Arcade CLI 1.17.1, in uv's own tool folder (`uv tool install arcade-mcp==1.17.1`), signed in with `arcade login` | `uv tool list` → `arcade-mcp v1.17.1` |
| The room | `C:\Dev\novel-door\.venv`, built by `setup.ps1`: the same sentence-transformers and torch as vector-snake | `SAME_TRANSLATOR` min cosine 1.000000 |
| The key | the GitHub App `novel-door-damian`, held by Arcade as `novel-door-github` | GitHub: two permissions, one repository |

**The key, least privilege:**

| GitHub App field | Set to |
| --- | --- |
| Callback URL | the Redirect URI on the saved Arcade provider's page |
| Request user authorization (OAuth) during installation | on (Arcade's recommendation) |
| Webhook → Active | off: the door calls GitHub; GitHub never calls back |
| Repository permissions | Issues: read and write · Metadata: read-only (on every app) · nothing else |
| Account permissions | none |
| Installed on | only `DamianGiambazi/novel-ssot` |

In Arcade (OAuth providers → Add → Included Providers → GitHub): ID `novel-door-github`, GitHub's Client ID (`Iv23...`) and a client secret. The secret goes from GitHub to Arcade and nowhere else.

**The config.** Claude Desktop's `claude_desktop_config.json` gets one block under `mcpServers`: which Python (`C:\Dev\novel-door\.venv\Scripts\python.exe`), which file (`server.py`) and the five settings above. Claude Desktop then starts the server itself. Its log is `%LOCALAPPDATA%\Claude\logs\mcp-server-novel_door.log`.

## The fair test, step by step

Same four questions, same chapters, same pass rules as Vault 2 (sealed 18 Oct). Only the method changes: who reads.

1. **Seal the prediction.** `PREDICTION-V3.md`, the two prompts and `seal-check-v3.ps1` are committed and pushed before the reader's first call. The Performance Edition predicts P1 4 of 4 held, P2 the reader reads the whole book (at least 20 of 24 chapters) and P3 the door: shut before sign-in, an issue after it, `SSOT.md` unchanged until the author commits. `seal-check-v3.ps1` then prints `SEALED_BEFORE_RUN` (no call has been made).

2. **Gate 1, the translator.** `translator_check.py` re-measures Vault 2's four questions in the new venv and compares them with the vectors from the day: `SAME_TRANSLATOR min cosine... >= 0.9999`.

3. **Gate 2, read the server.** The four tools, the four rules, what it can't see.

4. **Gate 3, talk MCP before any client.** `mcp_smoke.py` starts the server as Claude Desktop would, lists the tools and calls each one. Q1 must come back as Vault 2's `[1, 7, 24, 19]` at 0.5717 · 0.5758 · 0.5851 · 0.5940, the door must say `shut: sign-in required`, and no reply may hold a vector: `MCP_SMOKE_OK`.

5. **Open the reader.** Start Claude Desktop; `wait-for-door.ps1` prints the server's startup notes until `DOOR_RUNNING`.

6. **The fair-test checklist, before the prompt:** a chat, not a Code or Cowork session (those can read the laptop's files, and the answers are on it); a new chat, opened after Running, in no project; `novel_door` the only connector (Claude in Chrome off); web search off; Tool access "Tools already loaded"; memory and past chats off.

7. **The run.** `V3-PROMPT.txt` pasted verbatim; the reader uses the tools as it likes and ends with four lines, `Q1:` to `Q4:`. One run is the result; it is voided only if the model used the web or a tool was refused, and then said aloud.

8. **Score.** `score.py` applies Vault 2's rules to those four lines: `V3_SPINE_OK 4/4` or `V3_SPINE_PARTIAL n/4`.

9. **Audit.** `duckdb -bail -f calls.sql` lists every call, prints the reader's strategy (`READER reads=... meaning_searches=... -> READ_WHOLE_BOOK or SELECTIVE_READER`) and the firewall verdict `FIREWALL_HELD... vectors_out=0`. The seal check runs again: sealed before the first call.

10. **The door.** `AMEND-PROMPT.txt` asks for one SSOT amendment. The first call returns a sign-in link; after the author approves, the issue appears.

11. **The author declares.** In the browser, the author writes the rule in their own words and commits with `closes #n`; `git pull` brings it down.

A last check names what changed on the machine: one copy of each tool, and the user PATH, vector-snake's packages and uv's tools compared with the day's snapshot.

## The proof

Four of four held, where the laptop alone found one, and nothing but text left the laptop. Rehearsal results, 3 Nov 2026, Opus 5.5 (Medium) in Claude Desktop. The performance's numbers replace these before publication.

**The spine: `V3_SPINE_OK 4/4`.** The prediction was committed and pushed at 15:09:04 UTC; the first call came at 17:07:40 UTC: `SEALED_BEFORE_RUN`.

| Thread | Predicted (pass rule) | Reader's top 4 | Hits | Vault 2, laptop alone |
| --- | --- | --- | --- | --- |
| The watcher | 1 · 7 · 19 · 24 (3 of 4) | 19 · 7 · 1 · 24 | 4 of 4 | held |
| The lie | 2 · 5 · 13 · 21 (2 of 4) | 5 · 21 · 2 · 6 | 3 of 4 | not held |
| The cost | 4 · 5 · 7 (2 of 3) | 5 · 4 · 9 · 20 | 2 of 3 | not held |
| The door | 22 · 23 · 24 (2 of 3) | 24 · 23 · 22 · 10 | 3 of 3 | not held |

**How it read: the whole book.** 24 calls, all `read_chapter`, chapters 1 to 24 in order, in 37 s. No meaning search, no keyword search. The book is about 11,000 characters, small enough to fit on the reader's desk, so it took every book off the shelf. The laptop's search still works (Gate 3 reproduced Vault 2 to four decimals); the reader simply didn't need it. Search earns its place when the library outgrows the desk.

**What crossed:** `FIREWALL_HELD calls=24 vectors_out=0 chars_out=10927`.

**The door.** Before sign-in the smoke test printed `DOOR shut: sign-in required`. After the author's sign-in, issue #1 appeared: "[SSOT proposal] Add a state log for the middle dresser drawer (lock, letter, Sarah's tea)", citing chapters 4, 5, 6, 9, 13 and 20. It found the same continuity error the Vault 2 snags flagged by eye: Sarah's tea on the counter in chapter 6, back in the locked drawer in 9 and 20.

**The author declares.** The author wrote the rule in their own words and committed `a3fc6e3 docs: adopt the drawer state log from #1, in the author's words (closes #1)`. `git pull` → `Fast-forward`, `SSOT.md | 1+`; the issue closed itself.

**The machine, changed only as named.** One copy each of DuckDB, the HF CLI, Ollama, git, uv, Arcade and Gitleaks. The user PATH was unchanged. vector-snake's packages matched Vault 2's 30 Oct snapshot. uv's tools gained only `arcade-mcp v1.17.1`.

**The rehearsal's record is kept.** For the performance, `main` returns to the end of Vault 2 (`dc9e692`). The rehearsal stays on branch `v3-rehearsal` and in issue #1, closed, so the performance's issue is #2.

**Performance results: pending** (to be filled from the recorded take).

## What the work taught us

Each snag below was real, found in rehearsal on SPOOKY, diagnosed from its evidence and fixed at its source. Part Two of the video tells them in this order.

| Snag | What it teaches |
| --- | --- |
| The scorer read "Q2: 2, 5, 13, 21." (a full stop) as missing | test the judge before the trial |
| The plug test froze: memory flat, CPU flat, no reply; the model was loading in a background thread | never stack two unknowns, inside a program too |
| Byte 0x97 crashed the client: an em dash sent in Windows' old alphabet | "works on my machine" includes the alphabet |
| Claude Desktop said Failed: it starts the server twice, and one copy gives up after 37 s | a client may start you twice; never share a writable file between copies |
| A Code session, an attached project and the Chrome connector could each have shown the reader the answers | a fair test is a checklist, not an intention |
| GitHub answered 403 Forbidden: Arcade had used its own GitHub app, because ours was never saved | check which key was used, not just that a key exists |
| Asked to try again, the chat repeated its earlier message; the log showed no call | a model's account of what it did is not a log |
| A new chat couldn't find the tools ("Load tools when needed") | open the chat after Running, with tools already loaded |
| Vault 2's pip guard blocked `pip freeze` in the machine check | lift a guard for one read-only command, then restore it |
| The reader read the whole book and never searched | a surprise is data: the thesis changed and became a sealed prediction |

## Errata for the videos

None yet. This section is filled after the recording, using the IDs V3-E01 onwards, and mirrors Section A of `VAULT-3-ERRATA.md`.

| ID | Video | Said | Correct |
| --- | --- | --- | --- |
|  |  |  |  |

## Assets in this vault

Every file is listed, in order of use, in `VAULT-3-INDEX.md`:

- the door: `server.py` 1.1.4, `setup.ps1`, the config block;
- the gates: `translator_check.py`, `mcp_smoke.py`, `calls.sql`, `score.py`, `seal-check-v3.ps1`;
- the prompts: the sealed prediction and both prompt templates;
- the scripts around the take: `wait-for-door.ps1`, `reset-to-v2.ps1`, `restore-machine-v2.ps1`;
- the record: the rehearsal ledger, and the public repository [github.com/DamianGiambazi/novel-ssot](https://github.com/DamianGiambazi/novel-ssot) with its `v3-rehearsal` branch.

vector-snake itself is available on request.

## Glossary

| Term | Meaning here |
| --- | --- |
| MCP | Model Context Protocol: a standard plug between an AI client and a tool |
| MCP server | a program that offers tools through MCP; here, `novel_door` |
| client | the app that uses the tools; here, Claude Desktop |
| stdio | the client starts the server and talks to it through its input and output, not the network |
| tool | one function the server offers, with a name, inputs and a reply |
| Arcade | the framework that builds the server, and the service that holds its GitHub key |
| GitHub App | a key cut for chosen repositories and permissions, installed by the owner |
| OAuth provider | Arcade's record of a GitHub App: its ID, Client ID and secret |
| Redirect URI / callback URL | the address GitHub sends you back to after you approve |
| token | the short-lived proof of your approval that lets the tool write; never shown to the model |
| least privilege | give a key only the access its one job needs |
| issue | a note on a GitHub project; changes no files |
| `closes #n` | words in a commit message that close issue n and link the two |
| the library | the laptop's role: keep the book and serve it, text only |
| the reader | the model that reads the text and decides what it means |
| firewall | the rule that only text, never vectors, crosses to the client |
| call log | `calls.jsonl`: one line per tool call, audited by DuckDB |
| fair-test checklist | the settings that keep the reader from seeing the answers |
| workshop | the installs and key built once and shown already built |
| rehearsal branch | `v3-rehearsal`: the first run's history, kept when main was reset |

## What comes next

Vault 4 lets the reader write. Given the SSOT, the Constitution and the Handover, a model drafts a chapter, and the same gates (a sealed prediction, an audit, the author's decision) catch where it goes beautifully wrong.