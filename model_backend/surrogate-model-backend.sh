#!/usr/bin/env bash

#SBATCH --job-name=surrogate-model-backend
#SBATCH --nodelist=skadi
#SBATCH --qos=verylong
#SBATCH --time=4-00:00:00
#SBATCH --mem=32GB
#SBATCH --cpus-per-task=2
#SBATCH --ntasks=1
#SBATCH --ntasks-per-core=1
#SBATCH --nodes=1-1

set -u

MIN_PROC_ID=$(numactl --show | grep physcpubind | cut -d' ' -f2)
readonly MIN_PROC_ID
readonly LOCAL_DIR="/local/${USER}"
readonly LOCAL_DOCKER_ROOT="${LOCAL_DIR}/docker-${MIN_PROC_ID}"

infosun_docker() {
    dockerd-rootless-infosun --data-root "${LOCAL_DOCKER_ROOT}" -- docker "$@"
}

# Create docker network if it doesn't exist
if ! infosun_docker network ls | grep -q surrogate-model-net; then
    infosun_docker network create --driver bridge surrogate-model-net
fi

# Create image
#infosun_docker build -t surrogate-model-backend ./../backend/

#infosun_docker save -o ./surrogate-model-backend.tar surrogate-model-backend
# Load image from .tar file
infosun_docker load -i ./surrogate-model-backend.tar
# Start container from image
infosun_docker run --rm --memory=200g --env-file settings.env -p 5001:5001 -v /scratch/$USER/replication_package/model_backend/log/:/var/log/ --network surrogate-model-net surrogate-model-backend



