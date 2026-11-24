# VAULT 3 — FINAL PACKAGE · read first

**Vault Three: The Research and Preparation Playbook** · *The Door: Your Laptop as a Library, Any AI as the Reader*
**Status (5 Nov 2026): final.** The performance is recorded, and its transcript and results are in this package. The workshop has its own section, and both Reference documents are exported to PDF.

**Thesis:** *"The laptop serves. The model reads. The author declares."*

## The result
| | |
|---|---|
| The spine | `V3_SPINE_OK 4/4`, where the laptop alone found 1 of 4 in Vault 2 |
| How it read | `READ_WHOLE_BOOK`: all 24 chapters read, plus 4 meaning searches |
| What crossed | 28 calls · `FIREWALL_HELD` · no vectors left the laptop |
| The door | shut until the author signed in; then issue **#2** on `novel-ssot` |
| The author | answered #2, adopted it and closed it; `git pull` brought the new SSOT down |
| The machine | one copy of every tool; nothing changed during the video |

All three sealed predictions held: P1 (4/4), P2 (the whole book) and P3 (the door).

## What's in the box
| Folder | For | Start with |
|---|---|---|
| `reference/` | anyone: what Vault 3 is, how it works, the proof, the errata | `Vault 3 — The Door Reference.pdf` |
| `performance/` | the Vault 3 video: plan, runbook, transcript, capture log, cards | `V3-PERFORMANCE-CAPTURE-LOG.md` |
| `workshop/` | the workshop video: how the door was built, what broke, each fix | `VIDEO 3W — THE WORKSHOP (SCRIPT v1.0).md` |
| `kit/` | the files as they sit on SPOOKY under `C:\Dev\` | `VAULT-3-INDEX.md`, section 3 |
| `diagrams/` | the door, plus the Vault 1, Vault 2 and vector-snake data flows | the `.svg` files (`.png` for video) |
| root | the index, the errata, this file | `VAULT-3-INDEX.md` |

## Two videos, one vault
1. **Vault 3, the performance** (recorded). Nothing is installed on camera. Every gate runs, the reader runs once and the door opens once. The transcript is `performance/V3-TRANSCRIPT-PERFORMANCE.txt`.
2. **Vault 3, the workshop** (to record). This is the beat sheet's Part Two, grown into its own video. It covers the first run on 3 Nov: snags S01–S09, the four fair-test near misses and the setup notes. Then 4–5 Nov: the reset, two new snags (S10, S11) and the reinstatement of the key. Script: `workshop/VIDEO 3W — THE WORKSHOP (SCRIPT v1.0).md`.

## Before you publish
1. **Errata.** Add `VAULT-3-ERRATA.md` section A to the video description, or as captions. It holds eight items (V3-E01 to E08); none changes a result.
2. **Fill the four evidence fields** in `performance/V3-PERFORMANCE-CAPTURE-LOG.md` (marked **⟶ evidence**) from `$HOME\v3-evidence\TAKE\`. The transcript doesn't show them: the seal hash, the reader's four lines, `chars_out` and the author's commit hash.
3. **Blur check:** emails, address bars, the Client ID, secrets, Redirect URIs and the 2FA screens in K.
4. **Shut the door:** after the take, revoke the GitHub sign-in (Authorized GitHub Apps) and the Arcade connected user. Then run `mcp_smoke.py` and expect `DOOR shut`. The App and the key stay; `workshop/V3-REINSTATE — GitHub App and Arcade Key.md` covers both if either is ever lost.

## Security (unchanged)
Never open `~\.arcade\credentials.yaml`. Never paste the client secret, a token or a sign-in link's query string. Clear the clipboard after copying a secret: `Set-Clipboard -Value ' '`.
