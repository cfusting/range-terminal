#!/usr/bin/env bash
# usage: build_models experiment_name data_path data_name range_operators? num_runs
EXP="${HOME}/efsresults/${3}/${1}"
mkdir -p "${EXP}/saved_models"
cp "${RTHOME}/modeling/evolutionary_feature_synthesis.py" "${EXP}"
for i in `seq 1 ${5}`
do
	seed=${RANDOM}
	qsub -N efs_${1}_${seed} -v data=${2},seed=${seed},experiment=${1},rangeoperators=${4},EXP=${EXP} \
	"${RTHOME}/HPC/evolutionary_feature_synthesis.sh"
	echo "Run ${i}: ${1} started with seed ${seed}"
done
