#!/usr/bin/env bash
# usage: build_models experiment_name data num_runs
last=`pwd`
for i in `seq 1 ${3}`
do
	seed=${RANDOM}
	qsub -N symbolic_${1}_${seed} -v data=${2},seed=${seed},experiment=${1} \
	"${RT_HOME}/jobs/ml/symbolic_regression.sh"
	echo "Run ${i}: ${1} started with seed ${seed}"
done
cd ${last}
