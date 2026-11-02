#!/usr/bin/env bash
# Corre solo T-protocolo con los directorios corregidos. Espera a que haya
# memoria libre antes de cada corte (la máquina comparte RAM con otros
# experimentos). Uso: correr_protocolo.sh prueba_texto|prueba_imagen|ood|texto|imagen [cortes]
set -u
W=/c/Users/aq99l/Projects/MAE-TMS-exp11fix
PY=/c/Users/aq99l/Projects/MAE-TMS/.venv/Scripts/python.exe
R=$W/results/experimento11_protocolo_corregido
export EXP11_OUT=$R/informe_script
export EXP11_RAW=$R/raw
export PYTHONIOENCODING=utf-8
MIN_KB=${MIN_KB:-5242880}
cd "$W"
mkdir -p "$R/logs"

libre_kb() {
  powershell.exe -NoProfile -Command "(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory" | tr -d '\r '
}

espera_memoria() {
  while true; do
    f=$(libre_kb)
    if [ "$f" -ge "$MIN_KB" ]; then
      echo "$(date '+%F %T') libre ${f} kB, sigue" | tee -a "$R/logs/memoria.log"
      return
    fi
    echo "$(date '+%F %T') esperando: ${f} kB libres" >> "$R/logs/memoria.log"
    sleep 180
  done
}

fase=$1
cortes=${2:-25,50,100,200}
comun=(--seeds 42-51 --workers "${WORKERS:-2}" --arms T-protocolo)
CHUNKS=${CHUNKS:-6}
case $fase in
  prueba_*) export EXP11_RAW=$R/prueba/raw EXP11_OUT=$R/prueba/informe_script ;;
esac
case $fase in
  prueba_texto)  extra=(--seeds 43 --chunks 6 --workers "${WORKERS:-2}" --arms T-protocolo); comun=() ;;
  prueba_imagen) extra=(--seeds 43 --image-only --chunks 6 --img-per-class 10 --workers "${WORKERS:-2}" --arms T-protocolo); comun=() ;;
  texto)  extra=(--chunks "$CHUNKS") ;;
  imagen) extra=(--image-only --chunks "$CHUNKS" --img-per-class 10) ;;
  ood)    extra=(--ood-only --ood-file results/experimento11/consultas_fuera_dominio.txt) ;;
  *) echo "fase desconocida: $fase"; exit 2 ;;
esac

IFS=, read -ra lista <<< "$cortes"
for c in "${lista[@]}"; do
  espera_memoria
  t0=$(date +%s)
  echo "$(date '+%F %T') inicio $fase N=$c" | tee -a "$R/logs/tiempos.log"
  "$PY" -u run_experiment11_monolithic.py --cuts "$c" "${comun[@]}" "${extra[@]}" \
      >> "$R/logs/${fase}_N${c}.log" 2>&1
  rc=$?
  echo "$(date '+%F %T') fin $fase N=$c rc=$rc $(( ($(date +%s) - t0) / 60 )) min" | tee -a "$R/logs/tiempos.log"
done
