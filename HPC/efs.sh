#!/usr/bin/env bash
#PBS -l nodes=1:ppn=1,pmem=20gb,pvmem=20gb
#PBS -l walltime=30:00:00
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -m p
source $HOME/.bash_profile
python ${RTHOME}/modeling/evolutionary_feature_synthesis.py -d ${data} -s ${seed} -e ${experiment} \
-m "${EXP}/saved_models" -r ${rangeoperators}
