# VIDEO 3W — THE WORKSHOP (SCRIPT v1.0)
## *"How the Door Was Built: three hours, eight fixes, one clean take"*
### Vault Three: The Research and Preparation Playbook · the companion video

**What this is:** the second Vault 3 video. The performance video shows the door working. This one shows how it was built and what broke, from the rehearsal's own evidence. It grows the Performance Edition's Part Two (DD1–DD8) to cover the full story: 3 Nov (the build), then 4–5 Nov (the reset, two new snags, the key re-checked) and the take.
**Source of every line:** `V3-REHEARSAL-LEDGER.md` (quotes are copied from the screen or the logs), `V3-REINSTATE — GitHub App and Arcade Key.md`, and the performance capture log.
**Form:** voice over the evidence: screenshots, log excerpts and a few live browser shots. Nothing is installed or run live except W12 and W13 (optional, read-only). **Runtime ≈ 15 min.**
**Assets:** `C:\Dev\v3-docs\deep-dive\` (runbook R-9), plus the four new ones marked **NEW** below.
**Blur:** every address bar, email, Client ID, secret, Redirect URI and 2FA screen. The Redirect URIs quoted in the ledger are shortened (`…44bi5ZYcIrv4`); never show a whole one.

**Each beat:** SEE (the evidence) · SAY (2–4 lines) · LESSON (the card line, from `V3-CARDS.md` §10).

---

## RUNTIME MAP
| Beat | | Time | Ledger |
|---|---|---|---|
| W0 | Cold open | 0:00–0:30 | |
| W1 | The plan, and the seal first | 0:30–1:30 | timeline 16:09 |
| W2 | Three installs | 1:30–2:30 | 16:19, W6 |
| W3 | The key | 2:30–4:00 | W1–W5 |
| W4 | Two things at once | 4:00–5:30 | S02, W7 |
| W5 | The wrong alphabet, and the twin | 5:30–7:00 | S03, S04 |
| W6 | The fair test nearly broke | 7:00–8:00 | F1–F4 |
| W7 | The finding | 8:00–9:00 | S05 |
| W8 | The wrong key | 9:00–10:30 | S06 |
| W9 | The reader that repeated itself | 10:30–11:30 | S07, S08 |
| W10 | My own guard | 11:30–12:00 | S09 |
| W11 | Reset the stage, keep the record | 12:00–13:00 | §4, DD8 |
| W12 | The first minute after a reboot, and the other folder | 13:00–14:00 | S10, S11 |
| W13 | When the key goes missing | 14:00–14:45 | REINSTATE |
| W14 | Close | 14:45–15:30 | |

---

## W0 · Cold open (30 s)
- **SEE:** issue #1 on `novel-ssot`, closed: *"[SSOT proposal] Add a state log for the middle dresser drawer (lock, letter, Sarah's tea)"*. Then the bug-ledger card (§10).
- **SAY:**
  - "This is issue number one. In the Vault 3 video you saw number two, filed first time, in one clean take."
  - "Number one took three hours and eight fixes. This is that afternoon."

## W1 · The plan, and the seal first (1 min)
- **SEE:** the timeline (ledger §1) as a card, then the seal commit `585cee9` at 16:09.
- **SAY:**
  - "The rule from Vault 1 holds: seal the prediction before you touch anything. 16:09, sealed and pushed. Not one Vault 3 tool was installed yet."
  - "The plan: install three things, cut one key, pass three gates, then let a frontier model read my book through a door I control."
- **LESSON:** *Seal before you build. Then nothing you learn can move the target.*

## W2 · Three installs (1 min)
- **SEE:** `uv tool install arcade-mcp==1.17.1` (16:19); `uv tool list`; `setup.ps1` building `C:\Dev\novel-door\.venv`; Claude Desktop's settings.
- **SAY:**
  - "Arcade's command line goes in uv's own tool folder, not my Python. One copy, one place."
  - "The door gets its own room: a venv with the same translator as Vault 2. The first gate proves it: minimum cosine 1.000000, the same numbers to six places."
  - "And Claude Desktop, the reader. Its logs aren't where the docs say: they're in Local AppData (W6)."
- **LESSON:** *The 100% rule: one copy of everything, in a place you can name.*

## W3 · The key (1.5 min) — W1–W5
- **SEE:** the GitHub App form with *"Please fill out this field"* on the webhook; Arcade's Redirect URI (blurred); the *"Authorization error … missing_parameters"* page.
- **SAY:**
  - "The door needs one key: my own GitHub App, allowed to write issues on one repository. Nothing else."
  - "GitHub's form wanted a webhook, a way for GitHub to call me. I don't need one: my door calls GitHub. Untick it."
  - "The return address comes from Arcade, the Redirect URI. After installing the App, Arcade showed an error, and it was the right error: nobody was waiting for that sign-in yet."
- **LESSON:** *Take only what you need. Read an error before you fix it.*

## W4 · Two things at once (1.5 min) — S02, W7
- **SEE:** the monitor (`337 MB · CPU flat · smoke calls logged : 0`, unchanged after 2 min), then the hand-run log line *"Loading SentenceTransformer model…"*, 58 s after start.
- **SAY:**
  - "Gate 3, the plug test, froze. Memory flat, CPU flat, no reply. Ctrl+C did nothing; Stop-Process did."
  - "Run by hand, the server took a minute just to load the translator. Version 1.1.0 did that in a background thread while it answered, and on Windows the two deadlocked."
  - "The fix: load first, then open the door. Slower to start, fast forever after: 0.2 s a search."
- **LESSON:** *Never stack two unknowns, inside a program too.*

## W5 · The wrong alphabet, and the twin (1.5 min) — S03, S04
- **SEE:** `UnicodeDecodeError … byte 0x97`; then Claude's **Failed** badge and the log lines `Request timed out { context: 'shared-pool' }` and `ready for a client (82.4 s)`.
- **SAY:**
  - "Next crash: byte 0x97. An em dash, sent in Windows' old alphabet instead of UTF-8. My test machine was Linux; it could never have shown me."
  - "Then Claude Desktop said Failed. It starts my server twice, once for chat and once for coding sessions, and the second copy gives up after 37 seconds. Both were writing the same index."
  - "Each copy now gets its own index and writes how far it got to the log. Version 1.1.3. The toast you may see is the second copy, and it's harmless."
- **LESSON:** *Works on my machine includes the alphabet. A client may start you twice.*

## W6 · The fair test nearly broke (1 min) — F1–F4
- **SEE:** the three screenshots: the Code session (`</>`, "This computer"); the project name under the chat box; Claude in Chrome switched on.
- **SAY:**
  - "Three ways the reader could have seen the answers: a coding session that reads my disk, a project that holds my notes, a browser that can open the public repo."
  - "I caught all three before pressing send. That's why the performance shows a checklist before the prompt."
- **LESSON:** *A fair test is a checklist, not an intention.*

## W7 · The finding (1 min) — S05
- **SEE:** the rehearsal's `calls.sql`: 24 `read_chapter` rows, chapters 1 to 24 in order, `FIREWALL_HELD calls=24 vectors_out=0 chars_out=10927`.
- **SAY:**
  - "Four of four, the first time. But the biggest surprise wasn't a bug. The reader never used my laptop's search. It read the whole book: eleven thousand characters fit on its desk."
  - "So my thesis changed. Not 'the laptop finds'. The laptop serves. In the performance I sealed that as a prediction, and it held: all 24 chapters again, this time with four quick searches first."
- **LESSON:** *Raw evidence beats description. A surprise is data.*

## W8 · The wrong key (1.5 min) — S06
- **SEE:** `POST … /issues "HTTP/1.1 403 Forbidden"`; Arcade's Connected users showing **arcade-github** (blur the email); the providers list without ours.
- **SAY:**
  - "The sign-in worked, then GitHub said Forbidden. The connected-users page showed why: Arcade had used its own GitHub app, not mine. My key had never been saved. I'd put the wrong thing in the Client ID box."
  - "GitHub refused a key that wasn't cut for this lock. Least privilege, working exactly as designed, against me."
  - "I saved the key properly, gave GitHub the new return address, and taught the server to print GitHub's exact reason next time. Version 1.1.4."
- **LESSON:** *Check which key was used, not just that a key exists.*

## W9 · The reader that repeated itself (1 min) — S07, S08
- **SEE:** two identical chat messages side by side; the MCP log with no call after 18:15:52; *"No matching tools found"*.
- **SAY:**
  - "I asked it to try again. It sent the same words as before, and the log showed it never called the tool."
  - "Then a new chat couldn't even find the door: it was set to look tools up on demand. Tools already loaded, a chat opened after Running, and it worked. 18:57, issue number one."
- **LESSON:** *A model's account of what it did is not a log.*

## W10 · My own guard (30 s) — S09
- **SEE:** `ERROR: Could not find an activated virtualenv (required).`
- **SAY:** "The last check, did I change the machine, was blocked by a guard I set myself in Vault 2. Good guard. I lift it for one read-only command, then put it back, and say so on camera."
- **LESSON:** *Write down when you lift a guard, and put it back.*

## W11 · Reset the stage, keep the record (1 min) — DD8
- **SEE (live, read-only):** GitHub branches: `main` and **`v3-rehearsal`** at `a3fc6e3`; the closed issue #1 with its comment. Then the `reset-to-v2.ps1` plan and `RESET_TO_V2_OK` (screenshot).
- **SAY:**
  - "It worked, but it was messy, and it ran on a public repository. So I made it the rehearsal."
  - "I put main back to the end of Vault 2 and deleted nothing. The rehearsal lives on a branch, and its issue is still number one. That's why the performance filed number two."
  - "Plans are scaffolding, not scripture. The first take was the scaffolding."
- **LESSON:** *Reset the stage, keep the record.*

## W12 · The first minute after a reboot, and the other folder (1 min) — S10, S11 · NEW
- **SEE (NEW):** Claude Desktop's log with torch still importing at 115.9 s, and novel_door **Failed**; then the preflight's FAIL on `claude_desktop_config.json` and the folder `%LOCALAPPDATA%\Claude-Data\claude_…\` (blur the user name).
- **SAY:**
  - "The day after, two new snags. After a reboot, the first start took almost two minutes just to load torch from a cold disk, and the chat gives up at two minutes. So before the take I warm the door with one smoke test."
  - "And my own gate said the config was missing. It wasn't: the Store version of Claude Desktop keeps it in a different folder. The gate now looks everywhere it can live."
- **LESSON:** *A cold start is a different machine. Look where the app actually keeps its files.*

## W13 · When the key goes missing (45 s) — REINSTATE · NEW
- **SEE (NEW):** the reinstatement guide's Step 0 table; `DOOR shut. Open this link…` → GitHub's *"Authorize novel-door-damian"* (blurred) → `DOOR_TEST_OK … HTTP 200`.
- **SAY:**
  - "Before the take I checked the key end to end without writing anything: a read-only door test. GitHub had to name my app, not Arcade's. HTTP 200, door test OK."
  - "Then I shut the door again, so the performance would show the first sign-in for real. If you ever lose the app or the key, the guide in the downloads walks through it, one change at a time."
- **LESSON:** *Prove the key without using it. Then put the stage back.*

## W14 · Close (45 s)
- **SEE:** the bug-ledger card (§10) with all ten rows; then the performance result card: `V3_SPINE_OK 4/4` · `READ_WHOLE_BOOK` · `FIREWALL_HELD` · issue #2.
- **SAY:**
  - "Eleven snags across three days. Each found from evidence, fixed one change at a time, at its source. Every one is in the downloads."
  - "The second take ran without a single new snag. That's what a rehearsal is for."
  - "The laptop serves. The model reads. The author declares."
  - "I'm Damian. This was the Vault 3 workshop, for AI Foundations."

---

## THE FIVE GOLDEN RULES, IN THIS VIDEO
| Rule | Where |
|---|---|
| Raw evidence beats description | W7 · W9 |
| Never stack two unknowns | W4 · W8 (one change at a time) |
| Plans are scaffolding, not scripture | W7 (the thesis) · W11 |
| Trust but verify | W8 (which key) · W13 (the door test) |
| Context is a budget, curate it | W6 (the fair test) |

## RECORDING NOTES
- Read numbers from the evidence, not from this sheet.
- W11 and W13 can be recorded live, but **read-only**: no new issue, no sign-in left open. After any W13 re-shoot, shut the door again (REINSTATE 5.4–5.6).
- Pause a frame on every lesson card. They are the bug ledger's rows in order.
