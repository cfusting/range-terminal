#!/usr/bin/env bash
#PBS -l nodes=1:ppn=1,pmem=2gb,pvmem=2gb
#PBS -l walltime=00:03:00
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
source $HOME/.bash_profile
export PYTHONPATH=$FASTSRHOME:$MLHOME:$FASTGPHOME
cd ${ARCTIC_RESULTS_HOME}/${folder}
python ${RTHOME}/modeling/symbolic_regression.py -d ${data} -s ${seed} -e ${experiment} -m "${RTHOME}/results" \
  -o "${RTHOME}/results/"
