# restore-machine-v2.ps1 — OPTIONAL (Path B): take the laptop itself back to the end of Vault 2.
# Run reset-to-v2.ps1 first. Off camera. Claude Desktop must be QUIT. Asks you to type RESTORE.
# Removes, in this order: the novel_door block from Claude Desktop's config (a backup is kept), the Arcade sign-in
# (arcade logout + ~\.arcade), the Arcade CLI (uv tool uninstall arcade-mcp), the door's venv and index.
# Keeps: C:\Dev\novel-door's source files, vector-snake, the V1/V2 stack, Gitleaks, Claude Desktop itself.
# Then compares the machine with $HOME\v3-snapshots\before-install (3 Nov, before Vault 3 installed anything).
param([switch]$Yes)
$ErrorActionPreference = 'Stop'
if (Get-Process claude -ErrorAction SilentlyContinue) { throw 'Claude Desktop is running: quit it from the tray icon first.' }
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
$cfgs = @("$env:APPDATA\Claude\claude_desktop_config.json", "$env:LOCALAPPDATA\Claude\claude_desktop_config.json") +
       @(Get-ChildItem "$env:LOCALAPPDATA\Claude-Data\*\claude_desktop_config.json" -ErrorAction SilentlyContinue | ForEach-Object FullName) +
       @(Get-ChildItem "$env:LOCALAPPDATA\Packages\*Claude*\LocalCache\Roaming\Claude\claude_desktop_config.json" -ErrorAction SilentlyContinue | ForEach-Object FullName)
$cfgs = @($cfgs | Where-Object { Test-Path $_ })
"THE PLAN"
"  Claude config(s)  : $(if ($cfgs) { $cfgs -join ', ' } else { 'none found' }) -> remove mcpServers.novel_door"
"  Arcade sign-in    : arcade logout; remove $HOME\.arcade"
"  Arcade CLI        : uv tool uninstall arcade-mcp"
"  door venv + index : C:\Dev\novel-door\.venv, index.lance"
if (-not $Yes) { if ((Read-Host 'Type RESTORE to continue') -ne 'RESTORE') { 'RESTORE_CANCELLED  nothing changed'; return } }
foreach ($c in $cfgs) {
    Copy-Item $c "$c.bak-$(Get-Date -Format yyyyMMdd_HHmmss)"
    $j = Get-Content $c -Raw | ConvertFrom-Json -AsHashtable
    if ($j.ContainsKey('mcpServers') -and $j.mcpServers.ContainsKey('novel_door')) {
        $j.mcpServers.Remove('novel_door')
        if ($j.mcpServers.Count -eq 0) { $j.Remove('mcpServers') }
        $j | ConvertTo-Json -Depth 50 | Set-Content $c -Encoding utf8NoBOM
        "  config: novel_door removed from $c (backup kept)"
    } else { "  config: no novel_door block in $c" }
}
if (Get-Command arcade -ErrorAction SilentlyContinue) { arcade logout 2>&1 | Out-Null }
Remove-Item "$HOME\.arcade" -Recurse -Force -ErrorAction SilentlyContinue
if (Get-Command uv -ErrorAction SilentlyContinue) { uv tool uninstall arcade-mcp 2>&1 | Out-Null }
Remove-Item C:\Dev\novel-door\.venv, C:\Dev\novel-door\index.lance -Recurse -Force -ErrorAction SilentlyContinue
""; "AFTER (compared with the 3 Nov before-install snapshot)"
$snap = "$HOME\v3-snapshots\before-install"
'duckdb','hf','ollama','git','uv','arcade','gitleaks' | ForEach-Object { "  $_ : $(@(Get-Command $_ -All -ErrorAction SilentlyContinue).Count)" }
$pathDiff = Compare-Object (Get-Content "$snap\userpath.txt") ([Environment]::GetEnvironmentVariable('Path','User') -split ';')
$uvDiff   = Compare-Object (Get-Content "$snap\uv-tools.txt") (uv tool list 2>$null)
"  user PATH diff : $(if ($pathDiff) { ($pathDiff | ForEach-Object { "$($_.SideIndicator) $($_.InputObject)" }) -join ' ; ' } else { 'none' })"
"  uv tools diff  : $(if ($uvDiff) { ($uvDiff | ForEach-Object { "$($_.SideIndicator) $($_.InputObject)" }) -join ' ; ' } else { 'none' })"
"  arcade sign-in : $(if (Test-Path "$HOME\.arcade") { 'STILL THERE' } else { 'gone' })   door venv : $(if (Test-Path C:\Dev\novel-door\.venv) { 'STILL THERE' } else { 'gone' })"
if (-not $pathDiff -and -not $uvDiff -and -not (Test-Path "$HOME\.arcade") -and -not (Test-Path C:\Dev\novel-door\.venv)) {
    'MACHINE_AT_V2  local installs removed. Manual steps left: delete the GitHub App, the Arcade provider, and (if wanted) Claude Desktop.'
} else { Write-Error 'MACHINE_NOT_AT_V2: see the AFTER lines' }
