# VAULT-3-INDEX — every file, in order of use

**Vault 3 · The Door** · final package, 5 Nov 2026 · laptop SPOOKY (Lenovo V15-IGL, Celeron N4020, 8 GB, Windows 11, PowerShell 7.6.9)
**Repository:** `github.com/DamianGiambazi/novel-ssot`: `main` (the take), branch `v3-rehearsal` (the rehearsal), issues #1 (the rehearsal) and #2 (the take).
**Personal data:** none in the kit. Paths are `C:\Dev\…` and `$HOME`; no email, Client ID, secret or Redirect URI appears anywhere.

## 1. Read
| File | What it is |
|---|---|
| `00-READ-FIRST.md` | the result, the folders, what's left before publishing |
| `reference/Vault 3 — The Door Reference.pdf` | **the reference guide** (13 pages): MCP and Arcade, the server, the workshop, the fair test step by step, the proof (performance and rehearsal), the lessons, the errata, the glossary. The live version is the Claude doc *Vault 3 — The Door: Reference* |
| `reference/Vault 3 — The Workshop Session Overview.pdf` | **the workshop at a glance** (6 pages): the 3 Nov timeline, the discovery and troubleshooting table, the reset and reinstatement, what it left |
| `VAULT-3-ERRATA.md` | eight corrections to the performance video (V3-E01–E08), with caption text; what changed after the take; what's open |

## 2. The two videos
### The performance (`performance/`)
| File | What it is |
|---|---|
| `VIDEO 3 — BEAT SHEET v4.0 (PERFORMANCE EDITION).md` | the script for chunks A–N (and DD1–DD8, now the workshop video) |
| `V3-RUNBOOK-PERFORMANCE.md` | the reset to the end of Vault 2 (R-1–R-9), the stage (P1–P7), recording, after the take, troubleshooting, rebuilding the workshop (Appendix A) |
| `V3-CARDS.md` | the on-screen cards, with the workshop bug-ledger card extended to S10 and S11 |
| `V3-TRANSCRIPT-PERFORMANCE.txt` | the published transcript of the take |
| `V3-PERFORMANCE-CAPTURE-LOG.md` | the take, recorded: every chunk, the three predictions judged, the snags; four evidence fields still to copy |

### The workshop (`workshop/`)
| File | What it is |
|---|---|
| `VIDEO 3W — THE WORKSHOP (SCRIPT v1.0).md` | **the workshop video's script**: W0–W14, about 15 min, voice over the rehearsal's evidence |
| `V3-REHEARSAL-LEDGER.md` | the source of every workshop line: the 3 Nov timeline, S01–S11, F1–F4, W1–W8, what changed and why, and the 4–5 Nov reset, reinstatement and take |
| `V3-REINSTATE — GitHub App and Arcade Key.md` | step by step: diagnose, reinstall or recreate the GitHub App, reinstate the Arcade key, prove it read-only (`DOOR_TEST_OK`), shut the door again |

The plan that actually ran on 3 Nov (the Live Edition beat sheet v3.0 and its runbook) is kept in the project under `claude/vault-3-live/v3-docs/`.

## 3. The kit (copy `kit\*` to `C:\Dev\`)
Order of use on the take day. Every script ends with one verdict word.

| # | File | Job | Verdict |
|---|---|---|---|
| 1 | `v3-preflight/reset-to-v2.ps1` | `main` back to `dc9e692`, the rehearsal kept on `v3-rehearsal` (asks you to type RESET) | `RESET_TO_V2_OK` |
| 2 | `v3-preflight/restore-machine-v2.ps1` | optional Path B: the laptop itself back to the end of Vault 2 (asks you to type RESTORE) | `MACHINE_AT_V2` |
| 3 | `v3-preflight/tab-header.ps1` | each new tab: `$BOOK`, `$DOOR_PY`, `$VS_PY`, `$MCP_LOG`, the Arcade provider; archives the last run's logs; starts the transcript | — |
| 4 | `v3-preflight/smoke-gitleaks.ps1` | no secret in the repository | `GITLEAKS_SMOKE_OK` |
| 5 | `v3-preflight/snapshot-v3.ps1` | tools, user PATH, vector-snake packages, uv tools (lifts the pip guard for one read-only command, S09) | `SNAPSHOT_OK` |
| 6 | `v3-preflight/memcheck.ps1` | free RAM while the stage is open | `MEM_OK` / `MEM_LOW` |
| 7 | `v3-preflight/preflight-check.ps1` | the gate: repository, venv, config (every known location, S11), Arcade, RAM (FAIL < 2.0 GB) | `PREFLIGHT_OK` |
| 8 | `novel-door/setup.ps1` | builds `C:\Dev\novel-door\.venv` (workshop only; pinned versions) | `VENV_OK` |
| 9 | `novel-door/claude_desktop_config.take.json` | the `novel_door` block for Claude Desktop's config | — |
| 10 | `v3-paste/spine/PREDICTION-V3.md` | the sealed prediction (Performance Edition): P1, P2, P3 and the fair-test conditions | — |
| 11 | `v3-paste/spine/V3-PROMPT.txt` · `AMEND-PROMPT.txt` | the reader's prompt (I) and the amendment prompt (K) | — |
| 12 | `v3-paste/spine/seal-check-v3.ps1` | seal time vs the first call (D and J) | `SEALED_BEFORE_RUN` |
| 13 | `novel-door/translator_check.py` | Gate 1: the venv measures like Vault 2 (E) | `SAME_TRANSLATOR` |
| 14 | `novel-door/server.py` | **the door**, build 1.1.4: four tools, text only, every call logged | — |
| 15 | `novel-door/mcp_smoke.py` | Gate 3: talks MCP like Claude Desktop (G); `--door-test` proves the key read-only | `MCP_SMOKE_OK` · `DOOR_TEST_OK` |
| 16 | `v3-preflight/wait-for-door.ps1` | H: shows the server's startup notes from Claude's log | `DOOR_RUNNING` |
| 17 | `novel-door/score.py` | I: Vault 2's rules applied to the reader's four lines | `V3_SPINE_OK` / `V3_SPINE_PARTIAL` |
| 18 | `novel-door/calls.sql` | J: every call, the reader's strategy, the firewall | `READ_WHOLE_BOOK` / `SELECTIVE_READER` · `FIREWALL_HELD` |
| 19 | `v3-preflight/capture-evidence.ps1` | after the take: the logs, score, audit, seal and Claude's MCP log into `$HOME\v3-evidence\<label>\` | `EVIDENCE_SAVED` |
| — | `novel-door/.gitignore` | keeps `.venv`, the index and logs out of git | — |

**Pinned versions:** `arcade-mcp` CLI 1.17.1 (uv tool) · `arcade-mcp-server` 1.33.0 · `lancedb` 0.40.0 · `sentence-transformers` 6.1.0 · `torch` 2.14.1 · all-MiniLM-L6-v2 (snapshot `1110a243…`, offline).
**Names that must match:** the Arcade provider ID `novel-door-github` (Arcade, the config, `tab-header.ps1`) · the GitHub App `novel-door-damian`, installed on `novel-ssot` only, with Issues read and write plus Metadata read.

## 4. Diagrams (`diagrams/`)
| File | Shows |
|---|---|
| `V3-DIAGRAM-the-door.svg` / `.png` | Vault 3: the library, the door, the reader, the key-holder, the record, the author |
| `V1-FLOW-the-100-percent-rule.svg` / `.png` | Vault 1's data flow |
| `V2-FLOW-the-ssot-library.svg` / `.png` | Vault 2's data flow |
| `VS-FLOW-vector-snake.svg` / `.png` | vector-snake's data flow |
| `make_flows.py` | regenerates the three flow diagrams |

## 5. Verdict words, in the order they appear
`RESET_TO_V2_OK` → `MCP_SMOKE_OK` (`DOOR shut`) → `PREFLIGHT_OK` → `SEALED_BEFORE_RUN` → `SAME_TRANSLATOR` → `MCP_SMOKE_OK` → `DOOR_RUNNING` → `V3_SPINE_OK 4/4` → `READ_WHOLE_BOOK` · `FIREWALL_HELD` → `SEALED_BEFORE_RUN` → issue #2 → the author's commit → the machine check → `EVIDENCE_SAVED`.
