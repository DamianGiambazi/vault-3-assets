# VAULT-3-ERRATA

**Scope:** what was said on camera in the Vault 3 performance video, checked against the transcript (T + line), the code and the call log. None of these corrections changes a result. The Reference already uses the correct versions.
**Use:** section A goes in the video description or as captions. Section B lists the documents changed after the take.

## A. Words on camera
| ID | Chunk | Said (T line) | Correct | Caption text |
|---|---|---|---|---|
| V3-E01 | C | "We have Claude Desktop, which uses a GitHub App" (T43–44) | Arcade uses the GitHub App on the write tool's behalf. Claude Desktop never holds the key, and the model never sees the token | *Correction: Arcade, not Claude Desktop, uses the GitHub App.* |
| V3-E02 | C | Arcade is "the read and write MCP tool"; "we have authorized GitHub" (T47–49) | Arcade holds the key for the one write tool; the three read tools need no sign-in and don't touch Arcade. In C the key is saved (the OAuth provider), not authorized: the door stays shut until K | *Correction: the key is set up here; it is authorized later, at the proposal.* |
| V3-E03 | E | the check "runs the entire local pipeline" (T67–68) | the translator gate re-measures Vault 2's four questions in the new venv (`SAME_TRANSLATOR`); the smoke test in G repeats the Q1 search | *Correction: this gate checks the translator, not the whole pipeline.* |
| V3-E04 | G | the local models, including the vector-snake vectorizer, are quantized (T88–90) | Vault 1's small generator models are quantised. The translator, all-MiniLM-L6-v2, runs as published | *Correction: the embedding model is not quantised.* |
| V3-E05 | G | the smoke test "prompts us to sign into GitHub. We sign in" (T90–91) | it reports `DOOR shut: sign-in required` and Arcade issues a link. Nothing is signed in at G: the first sign-in is at the write in K (P3.1) | *Correction: the smoke test only shows the door is shut; the sign-in comes later.* |
| V3-E06 | I | "We are going to use the same prompt as before" (T100) | the same four questions and pass rules as Vault 2. The prompt itself, `V3-PROMPT.txt`, is new: one connector, no web, four `Q` lines | *Same questions and rules as Vault 2; a new prompt for the reader.* |
| V3-E07 | I | Claude "managed to find the exact chapters" (T112–113) | each thread met its sealed pass rule (for example at least 3 of 4 for the watcher), so 4 of 4 threads held. The top four aren't required to match exactly | *Each thread met its sealed pass rule.* |
| V3-E08 | L | closing the issue "means I accept the update"; "automatic updates to our SSOT via an MCP server" (T148–152) | the server only proposes. The SSOT changes when the author adopts the proposal in `SSOT.md`; closing the issue records the decision. Nothing is automatic: the machine proposes, the author declares | *Correction: the AI proposes; only the author's change updates the SSOT.* |
| V3-E09 | L | "our remote SSOT has been updated"; "it pulls down our updated SSOT" (T153–157) | closing #2 recorded the decision only. #2 was closed by hand on 5 Nov, with the adoption's commit message posted as a comment; `SSOT.md` was unchanged until the author adopted it in `3c6359b` (9 Nov, found in Vault 4 as V4-S03). The pull brought nothing new | *Correction: closing the issue didn't change the SSOT. The author adopted it later, in commit 3c6359b.* |

**Checked and correct:** "28 calls", "meaning searches four times", "read all the chapters", "no vectors leaked", "firewall held" (T119–121) · issue #2 (T141) · four tools, three without sign-in (T72–75) · "4 out of 4" (T113).

## B. Documents changed after the take
| Document | Change |
|---|---|
| Vault 3 — The Door: Reference | status final; the performance results in The proof; snags S10 and S11; errata E01–E08; the assets list |
| Vault 3 — The Workshop Session: Overview | new section: reset, S10, S11, the reinstated key, the take |
| `V3-REHEARSAL-LEDGER.md` | S10, S11, the reinstatement and the take added |
| `kit/v3-preflight/preflight-check.ps1`, `restore-machine-v2.ps1` | search for the config under `Claude-Data` (S11); the RAM FAIL threshold set at 2.0 GB |
| Beat sheet v4.0 | a header note: Part Two became the workshop video |
| this file | V3-E09 added (11 Nov), found in Vault 4 (V4-S03); wording from `VAULT-4-ERRATA.md` §D |

## C. Open
| ID | What | Owner |
|---|---|---|
| O1 | copy the seal hash, the four Q lines, `chars_out` and the author's commit hash (**`3c6359b`, 9 Nov**: there was no adoption commit on the take day, see V3-E09) into the capture log from `$HOME\v3-evidence\TAKE\` | Damian |
| O2 | if the issue #2 title or chapters are worth showing, add them to the Reference's proof table | Damian / master session |
| O3 | where the package says #2 was adopted on the take day (`00-READ-FIRST.md` line 15, capture log row L, the rehearsal ledger's take row), add "adopted 9 Nov, `3c6359b`, see V3-E09". The Reference too, if it says the same | Damian / master session |
