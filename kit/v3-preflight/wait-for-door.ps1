# wait-for-door.ps1 — chunk H: after starting Claude Desktop, watch its MCP log until the door is open for a client.
#   C:\Dev\v3-preflight\wait-for-door.ps1            (prints the server's own startup notes as they arrive)
# The server needs 40–80 s on SPOOKY to load torch and MiniLM (V3-S02). Claude Desktop may start a second copy
# for Cowork/Code sessions; that one times out after ~37 s and shows a "couldn't start" toast: harmless (V3-S04).
param([string]$Log = "$env:LOCALAPPDATA\Claude\logs\mcp-server-novel_door.log", [int]$TimeoutSec = 240, [string]$Build = '1.1.4')
$start = if (Test-Path $Log) { @(Get-Content $Log).Count } else { 0 }
$t = [Diagnostics.Stopwatch]::StartNew(); $seen = $start; $version = $null; $ready = $false
while ($t.Elapsed.TotalSeconds -lt $TimeoutSec) {
    if (Test-Path $Log) {
        $lines = @(Get-Content $Log)
        if ($lines.Count -lt $seen) { $seen = 0 }                  # the log was rotated
        if ($lines.Count -gt $seen) {
            foreach ($ln in $lines[$seen..($lines.Count - 1)]) {
                if ($ln -match 'novel_door: (.+)') { "  {0,5:N0} s  {1}" -f $t.Elapsed.TotalSeconds, $Matches[1] }
                if ($ln -match 'Starting novel_door v(\S+)') { $version = $Matches[1]; "  {0,5:N0} s  server v{1}" -f $t.Elapsed.TotalSeconds, $version }
                if ($ln -match 'Starting session' -and $version) { $ready = $true }
            }
            $seen = $lines.Count
        }
    }
    if ($ready) { break }
    Start-Sleep 2
}
if ($ready -and $version -eq $Build) { "DOOR_RUNNING  novel_door v$version answered Claude Desktop after {0:N0} s" -f $t.Elapsed.TotalSeconds }
elseif ($ready) { Write-Error "DOOR_WRONG_BUILD  v$version is running, expected v$Build" }
else { Write-Error "DOOR_NOT_RUNNING after $TimeoutSec s: Settings > Extensions > novel_door > View logs" }
