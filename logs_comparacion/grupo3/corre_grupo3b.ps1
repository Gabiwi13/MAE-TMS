$py = 'C:\Users\aq99l\Projects\MAE-TMS\.venv\Scripts\python.exe'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUNBUFFERED = '1'
$dir = 'C:\Users\aq99l\Projects\MAE-TMS-una-hetero'
$logs = Join-Path $dir 'logs_comparacion\grupo3'
New-Item -ItemType Directory -Force $logs | Out-Null
Set-Location $dir
$rasgos = 'C:\Users\aq99l\Projects\MAE-TMS-exp18\results\experimento18\rasgos'
$casos4 = 'color:apple,color:horse,patron:cow,pelo:dog'
# nombre, variables de entorno, argumentos
$jobs = @(
    @('exp18', @{}, @('run_experiment18_attributes.py', '--workers', '4')),
    @('exp18_propio_color', @{EXP18_RAW = "$dir\results\experimento18\filas_propio_color.json"; EXP18_CASES = 'color:apple,color:horse'},
        @('run_experiment18_attributes.py', '--workers', '4')),
    @('exp18_resnet18_in', @{EXP18_RAW = "$dir\results\experimento18\filas_resnet18_in.json"; EXP18_CASES = $casos4;
        EXP18_LAT = "$rasgos\latentes_resnet18_in_pca64.npy"; EXP18_STATS = "$rasgos\stats_resnet18_in_pca64.json"},
        @('run_experiment18_attributes.py', '--workers', '4')),
    @('exp18_tol_propio', @{EXP18_RAW = "$dir\results\experimento18\filas_tol_propio.json"; EXP18_CASES = $casos4; EXP18_TOL = '1'},
        @('run_experiment18_attributes.py', '--workers', '4')),
    @('exp18_tol_resnet18_in', @{EXP18_RAW = "$dir\results\experimento18\filas_tol_resnet18_in.json"; EXP18_CASES = $casos4; EXP18_TOL = '1';
        EXP18_LAT = "$rasgos\latentes_resnet18_in_pca64.npy"; EXP18_STATS = "$rasgos\stats_resnet18_in_pca64.json"},
        @('run_experiment18_attributes.py', '--workers', '4')),
    @('exp13', @{}, @('run_experiment13_augmentation.py', '--seeds', '42-46', '--workers', '2')),
    @('exp13_reporte', @{}, @('run_experiment13_augmentation.py', '--report-only')),
    @('exp16', @{}, @('run_experiment16_leave_object_out.py', '--folds', '1-10', '--workers', '2')),
    @('exp16_reporte', @{}, @('run_experiment16_leave_object_out.py', '--report-only'))
)
$vars = 'EXP18_RAW', 'EXP18_CASES', 'EXP18_LAT', 'EXP18_STATS', 'EXP18_TOL'
foreach ($j in $jobs) {
    foreach ($v in $vars) { Remove-Item "Env:$v" -ErrorAction SilentlyContinue }
    foreach ($k in $j[1].Keys) { Set-Item "Env:$k" $j[1][$k] }
    $t = Get-Date
    & $py @($j[2]) *> (Join-Path $logs "$($j[0]).log")
    "$($j[0]) rc=$LASTEXITCODE $([int]((Get-Date) - $t).TotalMinutes) min" | Add-Content (Join-Path $logs 'tiempos.txt')
}
