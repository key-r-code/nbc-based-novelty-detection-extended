#!/bin/bash
### select the partition "def"
#SBATCH --partition=def-sm
### set email address for sending job status
#SBATCH --mail-user=kr3288@drexel.edu
### account - essentially your research group
#SBATCH --account=rosenfreeprj
### select number of nodes
#SBATCH --nodes=1
### select number of tasks per node (threads)
#SBATCH --ntasks-per-node=1
### request 12 hours of wall clock time
#SBATCH --time=12:00:00
### memory size required per node (memory)
#SBATCH --mem=93GB
#SBATCH --cpus-per-task=24

. ~/.bashrc
start=`date +%s`

cd /ifs/groups/rosenMRIGrp/kr3288/extended/DM_pipeline_basic

snakemake --cores 24 --forceall

runtime=$((end-start))
echo "run time: $runtime"