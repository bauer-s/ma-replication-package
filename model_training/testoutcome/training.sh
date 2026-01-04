#!/usr/bin/env bash
#
#SBATCH --job-name=ggnn-classification
#SBATCH --nodelist=skadi
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --time=2-00:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=32GB
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --requeue

set -euo pipefail

# Paths
readonly CONDA_BASE="/scratch/$USER/miniconda3"
readonly CONDA_ENV="ggnn-env"
readonly SCRIPT_PATH="/scratch/$USER/replication_package/model_training/testoutcome/training.py"
readonly REQS_FILE="/scratch/$USER/replication_package/environment/requirements.txt"

export PIP_CACHE_DIR="/scratch/$USER/pip-cache"

# Prevent conda from using home directory for config, pkgs, envs
export CONDARC=/dev/null
export CONDA_PKGS_DIRS="/scratch/bauers/miniconda3/pkgs"
export CONDA_ENVS_DIRS="/scratch/bauers/miniconda3/envs"
export HOME="/scratch/bauers"

# Accept Anaconda ToS for required channels
"$CONDA_BASE/bin/conda" tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
"$CONDA_BASE/bin/conda" tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# Force full rebuild if requested
if [ "${FORCE_REINSTALL:-0}" = "1" ]; then
  echo "FORCE_REINSTALL=1: removing existing conda environment $CONDA_ENV"
  "$CONDA_BASE/bin/conda" remove -y -n "$CONDA_ENV" --all
  "$CONDA_BASE/bin/conda" create -y -n "$CONDA_ENV" python=3.11
  "$CONDA_BASE/bin/conda" run -n "$CONDA_ENV" pip install --upgrade pip
  "$CONDA_BASE/bin/conda" run -n "$CONDA_ENV" pip install --no-cache-dir -r "$REQS_FILE"
fi

# Create conda env if missing
if ! "$CONDA_BASE/bin/conda" info --envs | grep -q "$CONDA_ENV"; then
  "$CONDA_BASE/bin/conda" create -y -n "$CONDA_ENV" python=3.11
  "$CONDA_BASE/bin/conda" run -n "$CONDA_ENV" pip install --upgrade pip
  "$CONDA_BASE/bin/conda" run -n "$CONDA_ENV" pip install --no-cache-dir -r "$REQS_FILE"
else
  echo "Using existing conda environment $CONDA_ENV"
fi

# Activate conda environment
source "$CONDA_BASE/etc/profile.d/conda.sh"
conda activate "$CONDA_ENV"

# Parallelism settings for sklearn / numpy / MKL
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MKL_NUM_THREADS=$SLURM_CPUS_PER_TASK

: "${SAMPLE_FRAC:=1.0}"

echo "SAMPLE_FRAC=$SAMPLE_FRAC"
which python
python -V
pip list | grep -E 'pandas|scikit-learn|scipy|numpy|joblib' || true

echo "Starting classification training at $(date)"
python -u "$SCRIPT_PATH" || { echo "Classification training failed" >&2; exit 1; }
echo "Finished classification training at $(date)"
