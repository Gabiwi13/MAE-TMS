#!/usr/bin/env bash
# Exp19, reanudación: exp16 retoma desde los pliegues guardados; luego exp18.
set -e
cd "$(dirname "$0")"
PY=../MAE-TMS/.venv/Scripts/python.exe
OUT=results/experimento19
T=$OUT/tiempos.txt
step() {
  local name=$1; shift
  local t0=$(date +%s)
  "$@" 2>&1 | grep --line-buffered -v "oneDNN\|absl" >> $OUT/$name.log
  echo "$name rc=${PIPESTATUS[0]} $(( ($(date +%s) - t0) / 60 )) min" >> $T
}
EXP16_OUT=$OUT/exp16 step exp16 $PY run_experiment16_leave_object_out.py --folds 1-10 --workers 3
CASES=$($PY -c "
import run_experiment18_attributes as e
print(','.join(f'{a}:{c}' for c in e.CLASSES for a in ['color'] + e.axes_of(c)))" 2>/dev/null | tail -1)
EXP18_TOL=1 EXP18_LAT=$OUT/exp16/latentes.npy EXP18_RAW=$OUT/filas_exp18.json EXP18_CASES=$CASES \
  step exp18 $PY run_experiment18_attributes.py --workers 8
echo "listo" >> $T
