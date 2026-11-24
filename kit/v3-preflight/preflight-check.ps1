# preflight-check.ps1 — the last gate before the Performance take (off camera). Read-only: it changes nothing.
#   C:\Dev\v3-preflight\preflight-check.ps1
# Ends with PREFLIGHT_OK, or PREFLIGHT_FAIL and the lines to fix. 'info' lines never fail the gate.
# 4 Nov: also finds the Store app's config in %LOCALAPPDATA%\Claude-Data\claude_<id>\ (found on SPOOKY); RAM floor 2.0 GB.
# It checks the state the reset leaves: the workshop built (venv, Arcade CLI and sign-in, config with novel_door),
# the novel at the end of Vault 2 (dc9e692, no Vault 3 seal), Claude Desktop QUIT (so F's smoke test runs alone).
$book = 'C:\Dev\novel-ssot'; $door = 'C:\Dev\novel-door'; $py = "$door\.venv\Scripts\python.exe"
$fails = [System.Collections.Generic.List[string]]::new()
function Check([string]$name, [bool]$ok, [string]$fix) {
    "{0}  {1}" -f $(if ($ok) { 'ok  ' } else { 'FAIL' }), $name
    if (-not $ok) { $fails.Add("$name -> $fix") }
}
function Info([string]$text) { "info  $text" }

# ---- The machine
Check 'PowerShell 7'                    ($PSVersionTable.PSVersion.Major -ge 7) 'open Windows Terminal with PowerShell 7'
Check 'TEMP and TMP = C:\Dev\tmp'       ($env:TEMP -eq 'C:\Dev\tmp' -and $env:TMP -eq 'C:\Dev\tmp') 'dot-source tab-header.ps1'
foreach ($t in 'duckdb','git','uv','arcade','gitleaks') {
    $n = @(Get-Command $t -All -ErrorAction SilentlyContinue).Count
    Check "$t : one copy ($n)" ($n -eq 1) "check the PATH for $t"
}
Check 'Arcade signed in (~\.arcade\credentials.yaml)' (Test-Path "$HOME\.arcade\credentials.yaml") 'arcade login'
Check 'snapshot day-of, taken today'    ((Test-Path "$HOME\v3-snapshots\day-of\vs-freeze.txt") -and
    (Get-Item "$HOME\v3-snapshots\day-of\vs-freeze.txt").LastWriteTime.Date -eq (Get-Date).Date) '.\snapshot-v3.ps1 -Name day-of'
Check 'novel-ssot-clone removed'        (-not (Test-Path 'C:\Dev\novel-ssot-clone')) 'Remove-Item C:\Dev\novel-ssot-clone -Recurse -Force'
$hub = if ($env:HF_HUB_CACHE) { $env:HF_HUB_CACHE } elseif ($env:HF_HOME) { "$env:HF_HOME\hub" } else { "$HOME\.cache\huggingface\hub" }
Check 'MiniLM in the Hugging Face cache' (Test-Path "$hub\models--sentence-transformers--all-MiniLM-L6-v2\snapshots") 'the translator must come from the cache vector-snake used'
$free = (Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue).FreePhysicalMemory / 1MB
if ($free -ge 2.5) { Check ("free RAM at least 2.5 GB ({0:N2} GB)" -f $free) $true '' }
elseif ($free -ge 2.0) { Info ("free RAM {0:N2} GB: under the 2.5 GB target, above the 2.0 GB floor (the rehearsal ran at 2.35). Close what you can" -f $free) }
else { Check ("free RAM at least 2.0 GB ({0:N2} GB)" -f $free) $false 'close the browser tabs you do not need, OBS preview off, VS Code closed (V3-S02 lesson)' }

# ---- The door (the workshop, built in the rehearsal)
Check 'door venv'                       (Test-Path $py) 'Path B was run: rebuild the workshop (runbook, Appendix)'
if (Test-Path $py) {
    $pk = uv pip list --python $py 2>$null | Out-String
    foreach ($p in 'arcade-mcp-server 1.33.0','lancedb 0.40.0','sentence-transformers 6.1.0','torch 2.14.1') {
        $name, $ver = $p -split ' '
        Check "venv: $p" ($pk -match "(?m)^$([regex]::Escape($name))\s+$([regex]::Escape($ver))") 'run setup.ps1 again'
    }
}
Check 'server.py is build 1.1.4'        ([bool](Select-String -Path "$door\server.py" -Pattern 'build 1\.1\.4' -Quiet -ErrorAction SilentlyContinue)) 'copy novel-door\server.py from the Performance pack'
Check 'mcp_smoke.py writes its own log' ([bool](Select-String -Path "$door\mcp_smoke.py" -Pattern 'smoke-calls.jsonl' -Quiet -ErrorAction SilentlyContinue)) 'copy novel-door\mcp_smoke.py from the pack'
Check 'score.py is the V3-S01 build'    ([bool](Select-String -Path "$door\score.py" -Pattern 'V3-S01' -Quiet -ErrorAction SilentlyContinue)) 'copy novel-door\score.py from the pack'
Check 'calls.sql has the READER line'   ([bool](Select-String -Path "$door\calls.sql" -Pattern 'READ_WHOLE_BOOK' -Quiet -ErrorAction SilentlyContinue)) 'copy novel-door\calls.sql from the pack'
Check 'no calls.jsonl / answers.txt yet' (-not (Test-Path "$door\calls.jsonl") -and -not (Test-Path "$door\answers.txt")) 'dot-source tab-header.ps1 (it archives them)'

# ---- The book (the end of Vault 2)
Check "book: $book"                      (Test-Path "$book\book\corpus\ch-24.md") 'see the runbook, Part 1'
if (Test-Path "$book\spine\corpus.parquet") {
    $rows = duckdb -csv -noheader -c "SELECT count(*) FROM '$($book -replace '\\','/')/spine/corpus.parquet'"
    Check "index: corpus.parquet has 29 passages ($rows)" ($rows -eq '29') 'the Vault 2 index is missing: stop'
} else { Check 'index: corpus.parquet' $false 'the Vault 2 index is missing: stop' }
Check 'index: questions.parquet'         (Test-Path "$book\spine\questions.parquet") 'the Vault 2 index is missing: stop'
if (Test-Path "$book\.git") {
    git -C $book fetch -q 2>$null
    Check 'repo: on branch main'             ((git -C $book branch --show-current) -eq 'main') 'git -C C:\Dev\novel-ssot switch main'
    Check 'repo: no uncommitted changes'     (-not (git -C $book status --porcelain)) 'commit or discard'
    Check 'repo: HEAD is dc9e692 (end of Vault 2)' ((git -C $book rev-parse --short HEAD) -eq 'dc9e692') 'run reset-to-v2.ps1'
    Check 'repo: level with GitHub'          ((git -C $book rev-parse HEAD) -eq (git -C $book rev-parse origin/main)) 'run reset-to-v2.ps1'
    Check 'repo: no Vault 3 seal yet'        (-not (Test-Path "$book\spine\PREDICTION-V3.md")) 'run reset-to-v2.ps1'
    $r = git -C $book ls-remote --heads origin v3-rehearsal
    Check 'repo: the rehearsal is kept on v3-rehearsal' ([bool]$r) 'run reset-to-v2.ps1 (it pushes the branch first)'
} else { Check "repo: $book is a git repository" $false 'stop: the Vault 2 working copy is missing' }

# ---- The reader
$cfg = @("$env:APPDATA\Claude\claude_desktop_config.json", "$env:LOCALAPPDATA\Claude\claude_desktop_config.json") +
       @(Get-ChildItem "$env:LOCALAPPDATA\Claude-Data\*\claude_desktop_config.json" -ErrorAction SilentlyContinue | ForEach-Object FullName) +
       @(Get-ChildItem "$env:LOCALAPPDATA\Packages\*Claude*\LocalCache\Roaming\Claude\claude_desktop_config.json" -ErrorAction SilentlyContinue | ForEach-Object FullName)
$cfg = @($cfg | Where-Object { Test-Path $_ })
Check 'Claude Desktop config found'      ([bool]$cfg) 'open Claude Desktop once: Settings > Developer > Edit Config'
$block = $null
foreach ($c in $cfg) { try { $j = Get-Content $c -Raw | ConvertFrom-Json -AsHashtable; if ($j.mcpServers.novel_door) { $block = $j.mcpServers.novel_door } } catch {} }
Check 'config: novel_door block present' ([bool]$block) 'paste claude_desktop_config.take.json''s block (runbook, Part 2)'
if ($block) {
    Check 'config: command is the door venv'       ($block.command -eq $py) 'fix "command" in the config'
    Check 'config: NOVEL_REPO = DamianGiambazi/novel-ssot'  ($block.env.NOVEL_REPO -eq 'DamianGiambazi/novel-ssot') 'fix the env block'
    Check 'config: NOVEL_GITHUB_PROVIDER = novel-door-github' ($block.env.NOVEL_GITHUB_PROVIDER -eq 'novel-door-github') 'fix the env block (V3-S06)'
}
Check 'Claude Desktop is QUIT (F runs the smoke test alone; H starts it)' (-not (Get-Process claude -ErrorAction SilentlyContinue)) 'tray icon > Quit'
Check 'no stray python (an old door copy)' (-not (Get-Process python -ErrorAction SilentlyContinue)) 'Get-Process python | Stop-Process -Force'
$paste = 'PREDICTION-V3.md','V3-PROMPT.txt','AMEND-PROMPT.txt','seal-check-v3.ps1' | Where-Object { Test-Path "C:\Dev\v3-paste\spine\$_" }
Check "paste files in C:\Dev\v3-paste\spine ($(@($paste).Count) of 4)" (@($paste).Count -eq 4) 'copy v3-paste from the pack'
Check 'PREDICTION-V3.md is the Performance Edition' ([bool](Select-String -Path 'C:\Dev\v3-paste\spine\PREDICTION-V3.md' -Pattern 'Performance Edition' -Quiet -ErrorAction SilentlyContinue)) 'copy v3-paste from the pack'
Info 'Not checkable from here (runbook R-4 to R-7): GitHub sign-in revoked · Arcade connected user revoked · issue #1 closed · Tool access "Tools already loaded"'
""
if ($fails.Count -eq 0) { "PREFLIGHT_OK  performance  book=$book" }
else { "PREFLIGHT_FAIL  $($fails.Count) to fix:"; $fails | ForEach-Object { "  - $_" } }
