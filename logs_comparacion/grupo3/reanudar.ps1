# Relanza el grupo 3 al iniciar sesión si quedó cortado por un reinicio.
$dir = 'C:\Users\aq99l\Projects\MAE-TMS-una-hetero\logs_comparacion\grupo3'
$corriendo = Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
    Where-Object { $_.CommandLine -match 'run_experiment1[368]' }
if ($corriendo) { exit }
"reanudado al iniciar sesión $(Get-Date -Format 'yyyy-MM-dd HH:mm')" | Add-Content (Join-Path $dir 'tiempos.txt')
& (Join-Path $dir 'corre_grupo3b.ps1')
"grupo 3 terminado $(Get-Date -Format 'yyyy-MM-dd HH:mm')" | Add-Content (Join-Path $dir 'tiempos.txt')
