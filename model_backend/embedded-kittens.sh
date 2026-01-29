#!/usr/bin/env bash

#SBATCH --job-name=embedded-kittens
#SBATCH --nodelist=skadi
#SBATCH --qos=verylong
#SBATCH --time=4-00:00:00
#SBATCH --mem=8GB
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

# Remove existing image
#infosun_docker rmi $(docker images | grep 'embedded-kittens')
# Load image from .tar file
infosun_docker load -i ./embedded-kittens.tar
# Start container from image
infosun_docker run --rm --name embedded-kittens-01 -p 5002:8080 --network surrogate-model-net embedded-kittens