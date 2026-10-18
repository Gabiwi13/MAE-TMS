#!/usr/bin/env bash
# Exp19: pipeline completo con el encoder congelado (ResNet18 IN + PCA64).
# Etapas 5-8, exp16 (10 pliegues) y exp18 (todos los ejes, con lectura tolerante).
set -e
cd "$(dirname "$0")"
PY=../MAE-TMS/.venv/Scripts/python.exe
OUT=results/experimento19
mkdir -p $OUT
T=$OUT/tiempos.txt
step() {  # nombre, comando...
  local name=$1; shift
  local t0=$(date +%s)
  "$@" 2>&1 | grep --line-buffered -v "oneDNN\|absl" > $OUT/$name.log
  echo "$name rc=${PIPESTATUS[0]} $(( ($(date +%s) - t0) / 60 )) min" >> $T
}
# Lo calculado con otro encoder no se reutiliza.
rm -f models/latent_energy_threshold.json models/instance_latents_*.json models/mem_dom_*.pkl models/agent_*.pkl models/tme.pkl
for s in stage5_fill stage6_interaction stage7_bidirectional stage8_mature; do
  step $s $PY -c "import sys; sys.path.insert(0, 'src'); import $s; $s.run()"
done
EXP16_OUT=$OUT/exp16 step exp16 $PY run_experiment16_leave_object_out.py --folds 1-10 --workers 4
CASES=$($PY -c "
import run_experiment18_attributes as e
print(','.join(f'{a}:{c}' for c in e.CLASSES for a in ['color'] + e.axes_of(c)))")
EXP18_TOL=1 EXP18_LAT=$OUT/exp16/latentes.npy EXP18_RAW=$OUT/filas_exp18.json EXP18_CASES=$CASES \
  step exp18 $PY run_experiment18_attributes.py --workers 8
echo "listo" >> $T
