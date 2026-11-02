#!/usr/bin/env bash
# Codificador sin pérdida de clase: etapas 5-8, fase B por imagen y exp16 (10 pliegues).
# A lo más dos procesos pesados: tras la etapa 5, la cadena 6-7-8 corre junto a exp16 1-5,
# y al terminar la cadena entra exp16 6-10.
set -e
cd "$(dirname "$0")/../.."
PY=../MAE-TMS/.venv/Scripts/python.exe
OUT=results/codificador_sin_clase
T=$OUT/tiempos.txt
export EXP16_OUT=$OUT/exp16 PYTHONUNBUFFERED=1
step() {
  local name=$1; shift
  local t0=$(date +%s)
  echo "$name inicio $(date '+%F %H:%M:%S')" >> $T
  "$@" 2>&1 | grep --line-buffered -v "oneDNN\|absl" > $OUT/$name.log
  local rc=${PIPESTATUS[0]}
  echo "$name rc=$rc $(( ($(date +%s) - t0) / 60 )) min (fin $(date '+%H:%M:%S'))" >> $T
  return $rc
}
s() { step $1 $PY -c "import sys; sys.path.insert(0, 'src'); import $1; $1.run()"; }

grep -q '"cls_weight": 0.0' models/encoder.meta.json || { echo "encoder.meta.json no declara cls_weight 0"; exit 1; }
# Lo calculado con otro codificador no se reutiliza.
rm -f models/latent_global_stats.json models/latent_energy_threshold.json models/instance_latents_*.json \
      models/mem_dom_*.pkl models/agent_*.pkl models/tme.pkl
T0=$(date +%s)
s stage5_fill
step tau $PY -c "import sys; sys.path.insert(0, 'src'); import stage7_bidirectional as s7; print(s7.latent_energy_threshold())"
( s stage6_interaction && s stage7_bidirectional && s stage8_mature \
  && step fase_b $PY $OUT/eval_fase_b.py . $OUT/filas_fase_b_sinclase.json \
  && until [ -f $EXP16_OUT/latentes_indice.json ]; do sleep 30; done \
  && step exp16_b $PY run_experiment16_leave_object_out.py --folds 6-10 --workers 1 ) &
CADENA=$!
step exp16_latentes $PY -c "import run_experiment16_leave_object_out as e; e.encode_all()"
step exp16_a $PY run_experiment16_leave_object_out.py --folds 1-5 --workers 1
wait $CADENA
step exp16 $PY run_experiment16_leave_object_out.py --report-only
echo "total $(( ($(date +%s) - T0) / 60 )) min" >> $T
