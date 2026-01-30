# Backend Repository

This folder contains helper scripts and image archives for running the surrogate-model backend and the Embedded-Kittens service used in the experiments.

1. Build **surrogate-model-backend.tar**
    1. Checkout the repository **bauers-ma** into any directory (outside this replication package).
    1. From this replication package, copy the trained models `mlp_best.joblib` and `mlp_classifier_best.joblib` (generated under `model_training/fitness/` and `model_training/testoutcome/`) into `bauers-ma/backend/files/trained_model/`.
    1. In the **bauers-ma** repository, build the Docker image and save it to a *.tar* file:
        ```sh
        docker build -t surrogate-model-backend backend/
        docker save -o ./surrogate-model-backend.tar surrogate-model-backend
        ```
    1. Copy the file `surrogate-model-backend.tar` into this directory `model_backend/`.

2. Build or provide **embedded-kittens.tar**
    - Build the Embedded-Kittens ("Litterbox Web") Docker image in its own repository and export it as `embedded-kittens.tar`, or reuse an existing archive.
    - Place `embedded-kittens.tar` into this `model_backend/` directory.

3. Configure service communication (`settings.env`)
    - This directory contains a `settings.env` file used by the startup scripts.
    - It defines environment variables such as hostnames and ports so that Embedded-Kittens and the surrogate model backend can talk to each other.
    - Adjust the values in `settings.env` if you run the services on different hosts or ports than in the original setup.

4. Start the services from this folder (`model_backend/`)
    - Start Embedded-Kittens:
        - `sbatch ./embedded-kittens.sh`
    - Start the surrogate-model backend:
        - `sbatch ./surrogate-model-backend.sh`

Once both services are running with a suitable `settings.env` configuration, you can start the Whisker cluster experiments (see `configs/` and the `whisker-cluster-experiments` repository for details).