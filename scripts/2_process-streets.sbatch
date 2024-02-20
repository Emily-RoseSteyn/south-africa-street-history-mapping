#!/bin/bash
#SBATCH --job-name=process_streets_emily
#SBATCH --output=logs/%x-%A_%a.out.log
#SBATCH --error=logs/%x-%A_%a.err.log
#SBATCH --cpus-per-task 1
#SBATCH --ntasks=12

# Python unbuffered for logs
export PYTHONUNBUFFERED=TRUE

# Assuming relative to root project directory
exec srun --unbuffered --mpi=pmi2 python ./src/street_list_preprocessing/main.slurm.py
