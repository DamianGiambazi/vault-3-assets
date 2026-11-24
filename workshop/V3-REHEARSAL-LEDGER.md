# V3-REHEARSAL-LEDGER — what the 3 Nov run taught us

**The run:** 3 Nov 2026, about 16:09–19:02 Berlin time, on SPOOKY, live, against the public `novel-ssot`. It started as the Live Edition take and is now treated as the rehearsal.
**Its record:**
- branch `v3-rehearsal` (seal `585cee9`, author's commit `a3fc6e3`);
- issue #1 (closed);
- `$HOME\v3-evidence\rehearsal-<date>\`: the call log, answers and Claude Desktop's MCP log.

**It ended:**
- `SAME_TRANSLATOR` · `MCP_SMOKE_OK` · `V3_SPINE_OK 4/4` · `FIREWALL_HELD calls=24 vectors_out=0 chars_out=10927` · `SEALED_BEFORE_RUN`;
- issue #1, closed by `a3fc6e3`;
- the machine unchanged except three named installs.

**This ledger is the source for the Vault 3 workshop video** (the beat sheet's Part Two, now its own video: `VIDEO 3W — THE WORKSHOP (SCRIPT v1.0).md`). Every quote below is copied from the screen or the logs.

---

## 1. Timeline (Berlin time)

| Time | What happened |
|---|---|
| 16:09 | Prediction sealed and pushed (`585cee9`), before any Vault 3 install |
| 16:19 | `uv tool install arcade-mcp==1.17.1` |
| ~16:50 | GitHub App created: webhook unticked, callback taken from Arcade |
| 17:00 | App installed on `novel-ssot` only. Arcade's page said *"Authorization error … missing_parameters"*: the expected, harmless error |
| 17:07 | Gate 1: `SAME_TRANSLATOR min cosine 1.000000` |
| 17:11–17:34 | Gate 3 hangs (**S02**); fixed in server 1.1.1 |
| 17:38 | Gate 3 crashes on byte `0x97` (**S03**); fixed in 1.1.2 |
| 17:41 | `MCP_SMOKE_OK`: Vault 2's four distances to the 4th decimal |
| 17:51 | Claude Desktop: **Failed** (`Request timed out`) (**S04**); fixed in 1.1.3 |
| 18:00 | Claude Desktop: **Running** |
| 18:01–18:05 | Fair-test near misses: a Code session, an attached project, Claude in Chrome on (**F1–F3**) |
| 18:07–18:08 | The reader reads all 24 chapters in order, 37 s, no search (**S05**) |
| 18:11 | `V3_SPINE_OK 4/4` |
| 18:15 | Proposal refused: `403 Forbidden` (**S06**) |
| 18:28 | Our Arcade provider actually created; callback updated |
| 18:34–18:53 | The old chat repeats itself and then loses the door (**S07**); "No matching tools found" (**S08**) |
| 18:47 | server 1.1.4 (GitHub's refusal reason, verbatim), applied as a PowerShell patch |
| 18:56 | Sign-in link → *"Authorization successful."* (it opened in Edge) |
| 18:57 | Issue #1 filed: *"[SSOT proposal] Add a state log for the middle dresser drawer (lock, letter, Sarah's tea)"* |
| 19:01 | Author's commit `a3fc6e3 … (closes #1)` · `git pull` → `SSOT.md \| 1 +` |
| 19:02 | Machine check passes (the pip guard needed lifting: **S09**) |

---

## 2. The snags (S = something broke; F = the fair test nearly broke; W = setup notes)

### S01 · The scorer misread tidy answers (found before the run, in the Live Edition pack)
- **Seen:** in testing, `"Q2: 2, 5, 13, 21."` (a full stop) and `"Q3: Ch 4, 5, 7, 14"` scored as MISSING.
- **Fix:** `score.py` reads chapter labels and punctuation, and the last labelled line counts. The rules are unchanged.
- **Lesson:** test the judge before the trial.

### S02 · Two things loading at once: the server froze (server 1.1.0 → 1.1.1)
- **Seen:** the smoke test hung. The monitor tab showed:
```
 8244    22     74 03/11/2026 17:11:30        free RAM : 0,94 GB    smoke calls logged : 0
 7972    21    337 03/11/2026 17:27:17        free RAM : 2,38 GB    smoke calls logged : 0   (2 min later: unchanged)
```
  Ctrl+C didn't stop it; `Stop-Process` did. Run by hand, the server started fine, but the model only began loading about **58 s** later: `INFO | 17:32:13 | Loading SentenceTransformer model…`.
- **Cause:** 1.1.0 loaded torch in a **background thread**. The first client request arrived mid-load, and the two deadlocked on Windows: memory flat, CPU flat, no reply.
- **Fix:** load torch and MiniLM **first, in the main thread**, before LanceDB or Arcade start any threads. Startup is slower (40–80 s on SPOOKY); every search is fast (0.2 s).
- **Lesson:** "Never stack two unknowns" applies inside a program too.

### S03 · The wrong alphabet down the pipe (1.1.1 → 1.1.2)
- **Seen:** `UnicodeDecodeError: 'utf-8' codec can't decode byte 0x97 in position 1894: invalid start byte`
- **Cause:** MCP speaks UTF-8. On Windows a pipe defaults to the old code page (cp1252), so an em dash `—` in a chapter went out as byte `0x97`. Nine of the 24 chapters contain such characters. The sandbox (Linux, UTF-8) could never have shown it.
- **Fix:** the server switches stdin and stdout to UTF-8 before reading or writing anything.
- **Lesson:** "works on my machine" includes the alphabet.

### S04 · Two copies, 37 seconds (1.1.2 → 1.1.3)
- **Seen:** Claude Desktop: **Failed** · *"Couldn't start for Cowork and Code sessions. Error: Request timed out"*. Its log:
```
16:47:15  Initializing server...
16:47:53  [error] Couldn't start for Cowork and Code sessions. Error: Request timed out { context: 'shared-pool' }
16:47:57  Message from client: method="initialize"          … no reply for 2 minutes
```
- **Cause:** Claude Desktop starts **two copies** of the server: one for chat, one for Cowork/Code. The Cowork/Code copy gives up after about 37 s, and our server needs 40–80 s. Both copies also rebuilt the **same** `index.lance` folder at once.
- **Fix:** each copy builds a **private index in TEMP**, deleted when it stops, and writes its progress to Claude's MCP log:
```
novel_door: torch + sentence-transformers imported (64.0 s)
novel_door: index ready: 29 passages (79.5 s)
novel_door: model loaded; ready for a client (82.4 s)
```
  The badge then read **Running**. The Cowork/Code toast still appears and is harmless: chat doesn't use that copy.
- **Lesson:** a client can start your server more than once; never let copies share a writable file.

### S05 · The reader read everything (a finding, not a bug)
- **Seen:** `calls.sql` showed **24 calls, all `read_chapter`, chapters 1 to 24 in order**, 10,927 characters, no search.
```
FIREWALL_HELD  calls=24  vectors_out=0  chars_out=10927
```
- **Meaning:** the book is small enough to read whole, so the reader never used the laptop's meaning search. The beat sheet's line "point at a search followed by a read" was impossible. The thesis "the laptop finds" was not shown.
- **Change:** the thesis becomes ***"The laptop serves. The model reads. The author declares."***, and the Performance Edition predicts the strategy (P2, `READ_WHOLE_BOOK`).
- **Lesson:** the audit caught what a description would have hidden. Raw evidence beats description. Search earns its place when the library is bigger than the reader's desk.

### S06 · The wrong key (Arcade provider; 1.1.3 → 1.1.4)
- **Seen:** the sign-in went through, then:
```
HTTP Request: POST https://api.github.com/repos/DamianGiambazi/novel-ssot/issues "HTTP/1.1 403 Forbidden"
Tool NovelDoor_ProposeSsotAmendment error: [UPSTREAM_RUNTIME_AUTH_ERROR] … (Forbidden, client error).
```
  Arcade → Connected users showed the sign-in under **`arcade-github`**. The OAuth providers list didn't contain `novel-door-github` at all.
- **Cause:** our provider was never saved. The form had been closed with the wrong Client ID in it, so Arcade used its own GitHub app, which isn't installed on `novel-ssot`. GitHub refused a key that wasn't cut for this lock.
- **Fix:** revoke the `arcade-github` sign-in. Create `novel-door-github` with the real Client ID (`Iv23…`) and a new secret. Copy **its** Redirect URI (a new one) into the App's Callback URL. 1.1.4 also reports GitHub's exact refusal: `GitHub refused: HTTP … | needs: … | token type: …`.
- **Lesson:** least privilege works: the wrong key failed safely. Check which key was used (Connected users), not just that a key exists.

### S07 · The reader that repeated itself
- **Seen:** after "Submit the proposal again", the chat gave a word-for-word copy of its earlier failure message. The MCP log showed **no tool call** after 18:15:52. After a Claude Desktop restart, the old chat reported that novel_door had disconnected.
- **Fix:** file the proposal from a **new chat**, opened after the door shows Running.
- **Lesson:** a model's account of what it did is not a log. Read the log.

### S08 · "No matching tools found"
- **Seen:** in a new chat started before the server was ready, the model searched for novel_door's tools and found none, although the connector switch was on.
- **Cause:** Tool access was set to **"Load tools when needed"**, which hides tools behind a search.
- **Fix:** Tool access **"Tools already loaded"**, and open the chat only after **Running**.

### S09 · My own guard blocked the machine check
- **Seen:** `ERROR: Could not find an activated virtualenv (required).` `PIP_REQUIRE_VIRTUALENV=true`, Vault 2's guard, stopped `pip freeze` in the global Python, so the 3 Nov snapshot never wrote `vs-freeze.txt`.
- **Fix:** lift the guard for that one read-only command, then restore it. `snapshot-v3.ps1` now does this. The comparison with Vault 2's 30 Oct snapshot was empty.
- **Lesson:** a good guard. Write down when you lift it, and put it back.

### F1–F4 · The fair test nearly broke (all caught before the prompt was sent)
| | What was on screen | Why it matters | Fix |
|---|---|---|---|
| F1 | A **Code** session (`</>` selected, "Choose environment", "This computer", a folder picker) | it can read files on the laptop, including `SSOT.md` and the predictions | the **chat** mode (speech bubble), New chat |
| F2 | The chat inside the project **"Vault Videos Cf_01"** | the project holds the SSOT, the predictions and the whole development history | no project |
| F3 | **Claude in Chrome** on in Connectors | it can browse the public repository, where the answers are | off; novel_door is the only connector |
| F4 | "Load tools when needed" | see S08 | "Tools already loaded" |

### W1–W8 · Setup notes (the workshop)
| | Note |
|---|---|
| W1 | GitHub App form: *"Please fill out this field"* on the Webhook URL → untick **Active**. The door calls GitHub; GitHub never calls us |
| W2 | The Callback URL comes **from Arcade**: Add OAuth Provider → Included → GitHub → ID → the Redirect URI shown in the form |
| W3 | Arcade's **Client ID** field takes GitHub's Client ID (`Iv23…`), not the provider name. This was the root of S06 |
| W4 | A Redirect URI shown in an unsaved form (`…fNGaGyVcbNuv`) belongs to a provider that doesn't exist yet. Use the one on the **saved** provider's page (`…44bi5ZYcIrv4`) |
| W5 | After installing the App, Arcade's page says *"Authorization error … missing_parameters"*. Expected: no sign-in was waiting |
| W6 | Claude Desktop's MCP log is `%LOCALAPPDATA%\Claude\logs\mcp-server-novel_door.log` (not `%APPDATA%`) |
| W7 | A hung smoke test ignores Ctrl+C: `Get-Process python \| Stop-Process -Force` from another tab |
| W8 | Arcade's sign-in link opens the **default** browser (Edge here), not the clean profile. Set the default, or blur |

---

## 3. What changed for the Performance Edition, and why

| Change | From |
|---|---|
| No installs, no GitHub App or Arcade setup on camera: the workshop is shown built (chunk C); how it was built is Part Two | operator, 3 Nov: "too ambitious" |
| `server.py` **1.1.4**, the build that ran the rehearsal's door, unchanged | S02 · S03 · S04 · S06 |
| New `wait-for-door.ps1`: H shows the server's startup notes until `DOOR_RUNNING` | S04 |
| Claude Desktop is **quit** before recording and started in H, so F's smoke test runs alone | S02 (memory) · S04 |
| The fair-test checklist on screen in H: chat · no project · only novel_door · web off · Tools already loaded | F1–F4 · S08 |
| A second, behavioural prediction (P2) and the `READER` line in `calls.sql` | S05 |
| Thesis: "The laptop serves. The model reads. The author declares." | S05 |
| `snapshot-v3.ps1` lifts the pip guard for `pip freeze` | S09 |
| `capture-evidence.ps1` copies Claude's MCP log from `LOCALAPPDATA` | W6 |
| `reset-to-v2.ps1`: main back to `dc9e692`, the rehearsal kept on `v3-rehearsal` | operator, 3 Nov: "a full return to baseline" |
| `restore-machine-v2.ps1` (optional): the laptop itself back to the end of Vault 2 | same |

---

## 4. After the rehearsal: reset, reinstate, perform (4–5 Nov)

| When | Step | Verdict |
|---|---|---|
| 4 Nov | `reset-to-v2.ps1`: plan shown, RESET typed, evidence archived, `v3-rehearsal` pushed, `main` back to `dc9e692` with `--force-with-lease` | `RESET_TO_V2_OK` |
| 4 Nov | R-3 to R-7: issue #1 commented; GitHub and Arcade sign-ins revoked; Claude set and quit; door shut | `MCP_SMOKE_OK` · `DOOR shut` |
| 4 Nov | first preflight: 3 FAILs (S10, S11 and low RAM) | fixed one at a time |
| 4 Nov | preflight after the S11 patch | `PREFLIGHT_OK` (RAM 2.24 GB, info) |
| 5 Nov | reinstatement of the App and the key (`V3-REINSTATE`): door test, sign-in, door test again | `DOOR_TEST_OK` (HTTP 200, nothing written) |
| 5 Nov | door shut again (5.4–5.6) | `DOOR shut` · `PREFLIGHT_OK` |
| take | the performance: `V3_SPINE_OK 4/4` · `READ_WHOLE_BOOK` (24 reads + 4 meaning searches) · 28 calls · `FIREWALL_HELD` · issue #2 adopted by the author | all three predictions held |

### S10 · The cold start (4 Nov)
- **Seen:** after a reboot, Claude Desktop's log showed the server still importing torch at 115.9 s. The chat lane gave up at about 120 s, so novel_door showed Failed. A second start took 53.8 s.
- **Cause:** the first import after a reboot reads torch from a cold disk, on a 2-core Celeron.
- **Fix:** warm the door before the take. Run one `mcp_smoke.py` (it loads the same files), stop it, then open Claude Desktop.
- **Lesson:** a cold start is a different machine. Rehearse the first minute after a reboot too.

### S11 · The config in the other folder (4 Nov)
- **Seen:** `preflight-check.ps1` said FAIL: no `claude_desktop_config.json` under `%APPDATA%\Claude\`, although Claude Desktop ran novel_door.
- **Cause:** the Microsoft Store build of Claude Desktop keeps its files in `%LOCALAPPDATA%\Claude-Data\claude_<id>\`.
- **Fix:** the gate and `restore-machine-v2.ps1` now search every known location (`%APPDATA%`, `%LOCALAPPDATA%\Claude`, `Claude-Data\*`, `Packages\*Claude*\LocalCache\Roaming\Claude`). The RAM check fails below 2.0 GB and shows an info line between 2.0 and 2.5 GB.
- **Lesson:** look where the app actually keeps its files. Never assume the documented path.

The next snag ID is V3-S12.
