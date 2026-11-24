# smoke-gitleaks.ps1 — Gitleaks is on the user PATH from an unrelated project (V3-STARTUP-01 §4).
# It stays; this records it like a Vault 1 install: one copy, a version, a smoke line.
$cmds = @(Get-Command gitleaks -All -ErrorAction SilentlyContinue)
"copies  : $($cmds.Count)"
if ($cmds.Count -ne 1) { Write-Error "GITLEAKS_SMOKE_FAIL  expected 1 copy, found $($cmds.Count)"; return }
$v = (gitleaks version 2>&1 | Out-String).Trim()
"version : $v"
"source  : winget package folder on the user PATH (not installed by any vault)"
if ($v) { 'GITLEAKS_SMOKE_OK' } else { Write-Error 'GITLEAKS_SMOKE_FAIL  no version printed' }
