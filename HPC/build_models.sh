#!/usr/bin/env bash
# usage: build_models experiment_name data_path data_name num_runs
EXP="${HOME}/rtresults/${3}/${1}"
mkdir -p "${EXP}/saved_models"
mkdir -p "${EXP}/logs"
mkdir -p "${EXP}/results"
cp "${RTHOME}/modeling/symbolic_regression.py" "${EXP}"
for i in `seq 1 ${4}`
do
	seed=${RANDOM}
	qsub -N symbolic_${1}_${seed} -v data=${2},seed=${seed},experiment=${1},EXP=${EXP} \
	"${RTHOME}/HPC/symbolic_regression.sh"
	echo "Run ${i}: ${1} started with seed ${seed}"
done
