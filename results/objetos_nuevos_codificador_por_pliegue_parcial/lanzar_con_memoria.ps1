# Lanza dos procesos sobre la cola de pliegues, cada uno solo si hay al menos 6 GB libres.
$root = 'C:\Users\aq99l\Projects\MAE-TMS-pliegues'
$py = 'C:\Users\aq99l\Projects\MAE-TMS\.venv\Scripts\python.exe'
$script = 'results\objetos_nuevos_codificador_por_pliegue\run_codificador_por_pliegue.py'
$logs = "$root\results\objetos_nuevos_codificador_por_pliegue\logs"
$log = "$logs\lanzamientos.txt"
$folds = '4,5,6,7,8,9,10'

function Log($msg) {
    $line = "{0} {1}" -f (Get-Date -Format s), $msg
    Write-Output $line
    for ($i = 0; $i -lt 10; $i++) {
        try { [IO.File]::AppendAllText($log, "$line`r`n"); return } catch { Start-Sleep -Milliseconds 500 }
    }
}

function Free-GB { (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB }

function Start-Lane($name) {
    $p = Start-Process -FilePath cmd.exe -WorkingDirectory $root -WindowStyle Hidden -PassThru `
        -ArgumentList '/c', "$py -u $script --folds $folds --cola > $logs\proceso_$name.txt 2>&1"
    Log ("{0}: lanzado (pid {1})" -f $name, $p.Id)
    return $p
}

while ($true) {
    $free = Free-GB
    Log ("A: {0:N2} GB libres" -f $free)
    if ($free -ge 6) { break }
    Start-Sleep -Seconds 120
}
$a = Start-Lane 'A'
Start-Sleep -Seconds 300
$b = $null
while (-not $a.HasExited) {
    $free = Free-GB
    Log ("B: {0:N2} GB libres" -f $free)
    if ($free -ge 6) { $b = Start-Lane 'B'; break }
    Start-Sleep -Seconds 120
}
$a.WaitForExit()
if ($b) { $b.WaitForExit() }
Log 'fin'
