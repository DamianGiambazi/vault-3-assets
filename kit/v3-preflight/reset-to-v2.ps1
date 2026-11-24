# reset-to-v2.ps1 — return the novel and the door to the end of Vault 2, keeping the rehearsal on the record.
# Off camera, once, before the Performance take. PowerShell 7. Claude Desktop must be QUIT (tray icon -> Quit).
#   C:\Dev\v3-preflight\reset-to-v2.ps1            # shows the plan, asks you to type RESET, then does it
# What it does (and nothing else):
#   1. archives the rehearsal's local evidence (call logs, answers, Claude's MCP log) to $HOME\v3-evidence\rehearsal-<date>
#   2. pushes the rehearsal's history to a branch, v3-rehearsal, so nothing is lost
#   3. moves GitHub's main back to dc9e692 (end of Vault 2) with --force-with-lease, then the local copy too
# What it does NOT do (the runbook's manual steps): issue #1, the GitHub sign-in, Arcade's connected user, Claude chats.
param([string]$Book = 'C:\Dev\novel-ssot', [string]$Door = 'C:\Dev\novel-door', [string]$Baseline = 'dc9e692',
      [string]$Branch = 'v3-rehearsal', [switch]$Yes)
$ErrorActionPreference = 'Stop'
if (Get-Process claude -ErrorAction SilentlyContinue) { throw 'Claude Desktop is running: quit it from the tray icon first (it holds the door open).' }
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Push-Location $Book
try {
    git fetch -q origin
    if (git status --porcelain) { throw "uncommitted changes in $Book : commit or discard them first" }
    $head   = git rev-parse --short origin/main
    $full   = git rev-parse origin/main
    $base   = git rev-parse --short "$Baseline^{commit}"
    git merge-base --is-ancestor $Baseline origin/main
    if ($LASTEXITCODE -ne 0) { throw "$Baseline is not an ancestor of origin/main: stop and check" }
    ""; "THE PLAN"
    "  GitHub main now : $head   ($(git log -1 --format=%s origin/main))"
    "  rehearsal kept  : branch $Branch -> $head  (commits since ${base}:)"
    git log --format='                    %h  %s' "$Baseline..origin/main"
    "  main goes back  : $base   ($(git log -1 --format=%s $Baseline))"
    "  evidence copied : $HOME\v3-evidence\rehearsal-$(Get-Date -Format yyyyMMdd)"
    if ($head -eq $base) { "NOTHING_TO_RESET  main is already at $base"; return }
    if (-not $Yes) { if ((Read-Host 'Type RESET to continue') -ne 'RESET') { 'RESET_CANCELLED  nothing changed'; return } }

    # 1. evidence
    $ev = "$HOME\v3-evidence\rehearsal-$(Get-Date -Format yyyyMMdd)"; New-Item -ItemType Directory -Force $ev | Out-Null
    foreach ($f in 'calls.jsonl','answers.txt','smoke-calls.jsonl') { if (Test-Path "$Door\$f") { Move-Item "$Door\$f" "$ev\$f" -Force } }
    $mcp = "$env:LOCALAPPDATA\Claude\logs\mcp-server-novel_door.log"
    if (Test-Path $mcp) { Copy-Item $mcp "$ev\mcp-server-novel_door.log" -Force }
    git log --format='%h  %cI  %s' -8 origin/main | Set-Content "$ev\git-log-before-reset.txt"
    Remove-Item "$Door\index.lance" -Recurse -Force -ErrorAction SilentlyContinue
    # 2. keep the rehearsal on GitHub
    git push origin "$($full):refs/heads/$Branch"
    # 3. main back to the end of Vault 2 (refuses if someone else moved main in the meantime)
    git push --force-with-lease="main:$full" origin "$($Baseline):main"
    git switch -q main
    git reset -q --hard $Baseline
    git fetch -q origin
    ""; "AFTER"
    "  local main  : $(git rev-parse --short HEAD)   origin/main : $(git rev-parse --short origin/main)   $Branch : $(git rev-parse --short origin/$Branch)"
    "  PREDICTION-V3.md in the book: $(Test-Path spine\PREDICTION-V3.md)"
    if ((git rev-parse --short HEAD) -eq $base -and (git rev-parse --short origin/main) -eq $base -and -not (Test-Path spine\PREDICTION-V3.md)) {
        "RESET_TO_V2_OK  main = $base · rehearsal kept on $Branch · evidence in $ev"
    } else { Write-Error 'RESET_INCOMPLETE: compare the AFTER lines with the plan' }
} finally { Pop-Location }
