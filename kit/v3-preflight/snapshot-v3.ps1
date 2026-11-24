# snapshot-v3.ps1 — record the machine before the take (off camera).
#   .\snapshot-v3.ps1 -Name day-of           # on the day, after the reset, before recording (M compares against it)
#   .\snapshot-v3.ps1 -Name after-restore    # only after the optional full machine restore (Path B)
# V3-S09 fix: PIP_REQUIRE_VIRTUALENV=true (Vault 2's guard) makes `pip freeze` refuse to run in the global Python,
# so the 3 Nov snapshot never wrote vs-freeze.txt. The guard is lifted for this one read-only command, then restored.
param([Parameter(Mandatory)][ValidateSet('day-of','after-restore','before-install')][string]$Name)
$VS_PY = "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.11.9\python.exe"
$dir = "$HOME\v3-snapshots\$Name"
New-Item -ItemType Directory -Force $dir | Out-Null
[Environment]::GetEnvironmentVariable('Path','User') -split ';' | Set-Content "$dir\userpath.txt"
$guard = $env:PIP_REQUIRE_VIRTUALENV
$env:PIP_REQUIRE_VIRTUALENV = $null
$freeze = & $VS_PY -m pip freeze
$env:PIP_REQUIRE_VIRTUALENV = $guard
if (-not $freeze) { Write-Error 'SNAPSHOT_FAIL: pip freeze printed nothing'; return }
$freeze | Set-Content "$dir\vs-freeze.txt"
uv tool list 2>$null | Set-Content "$dir\uv-tools.txt"
'duckdb','hf','ollama','git','uv','arcade','gitleaks' | ForEach-Object {
    "$_ : $(@(Get-Command $_ -All -ErrorAction SilentlyContinue).Count)"
} | Set-Content "$dir\tools.txt"
Get-Content "$dir\tools.txt"
"packages frozen: $(@($freeze).Count)"
"SNAPSHOT_OK  $Name  $(Get-Date -Format s)  -> $dir"
