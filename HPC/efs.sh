#!/usr/bin/env bash
#PBS -l nodes=1:ppn=1,pmem=2gb,pvmem=2gb
#PBS -l walltime=30:00:00
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -m p
source $HOME/.bash_profile
if [ "${rangeoperators}" == 'True' ]
  then
python ${RTHOME}/modeling/evolutionary_feature_synthesis.py -d ${data} -s ${seed} -e ${experiment} \
-m "${EXP}/saved_models" -r
  else
python ${RTHOME}/modeling/evolutionary_feature_synthesis.py -d ${data} -s ${seed} -e ${experiment} \
-m "${EXP}/saved_models"
fi
