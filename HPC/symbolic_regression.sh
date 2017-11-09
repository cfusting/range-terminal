#!/usr/bin/env bash
#PBS -l nodes=1:ppn=1,pmem=20gb,pvmem=20gb
#PBS -l walltime=05:00:00
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
source $HOME/.bash_profile
python ${RTHOME}/modeling/symbolic_regression.py -d ${data} -s ${seed} -e ${experiment} -m "${RTHOME}/saved_models" \
  -o "${RTHOME}/results"
