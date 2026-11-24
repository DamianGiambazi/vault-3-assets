# memcheck.ps1 — P2 memory bench. Start it, then use everything at once for the whole time:
# Claude Desktop with novel_door connected and a search running, OBS recording, the browser on GitHub.
#   .\memcheck.ps1 -Minutes 5
param([int]$Minutes = 5, [double]$FloorGB = 1.5)
$min = [double]::MaxValue
$end = (Get-Date).AddMinutes($Minutes)
while ((Get-Date) -lt $end) {
    $free = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB    # KB -> GB
    $min = [math]::Min($min, $free)
    "{0:HH:mm:ss}  free {1:N2} GB   lowest {2:N2} GB" -f (Get-Date), $free, $min
    Start-Sleep 5
}
if ($min -ge $FloorGB) { "MEM_OK   lowest free {0:N2} GB >= {1} GB" -f $min, $FloorGB }
else { "MEM_LOW  lowest free {0:N2} GB < {1} GB: close the browser tabs, lower OBS to 720p30, retest" -f $min, $FloorGB }
