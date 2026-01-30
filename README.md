# Replication Package

This repository contains the replication package for the surrogate-model-based automatic repair experiments.
It bundles:

- The environment specification
- Scripts to preprocess program variants and create the model training data
- Training scripts for the surrogate models
- Instructions to build and run the backend services
- Notebooks and data to regenerate the thesis tables and figures

## High-level workflow

1. **Set up the environment**
    - Create and activate the Conda environment as described in `environment/README.md`.

2. **Prepare program variants**
    - Place already generated variants (mutated program versions) and the corresponding `results.csv` into `variants/` as described in `variants/README.md`.

3. **Create model training data**
    - Use the scripts in `variants_out/` to
      - filter the raw `results.csv` for the selected projects,
      - call the Embedded-Kittens microservice and the GGNN embedding tool, and
      - merge embeddings with the repair results into a single dataframe.
    - The combined dataframe is written to `model_training/df.pickle`.

4. **Train surrogate models**
    - In `model_training/fitness/` run `training.py` to train the fitness regression model.
    - In `model_training/testoutcome/` run `training.py` to train the test-outcome classifier.
    - Both scripts read `df.pickle` and produce `mlp_best.joblib` and `mlp_classifier_best.joblib`.

5. **Build and start backend services**
    - Follow `model_backend/README.md` to build the Docker image for the surrogate-model backend and prepare the Embedded-Kittens image.
    - Copy the trained `*.joblib` files from `model_training/` into the backend repository (`bauers-ma/backend/files/trained_model/`) before building the image.
    - Start `embedded-kittens.sh` and `surrogate-model-backend.sh` from `model_backend/`.

6. **Run Whisker cluster experiments**
    - Checkout the external repositories:
      - `whisker` (branch `automatic-repair-surrogate-model`)
      - `whisker-cluster-experiments`
    - Copy the JSON config files from `configs/` into the `configs/` folder of `whisker-cluster-experiments`.
    - Run the cluster experiments to generate the raw experiment logs (baseline and surrogate-model runs).

7. **Analyze and reproduce thesis results**
    - Copy the raw experiment logs from the cluster into `temp_results/` (see `temp_results/README.md`).
    - Use the notebooks in `results/` to aggregate the raw logs into CSV files and to regenerate the LaTeX tables and figures used in the thesis.

## Folder overview

- `environment/`: Conda environment and Python dependencies for the replication package.
- `configs/`: JSON configuration files for the Whisker cluster experiments.
- `variants/`: Input variants and the corresponding `results.csv` file created by Whisker.
- `variants_out/`: Scripts that combine `results.csv` with program embeddings produced by Embedded-Kittens + GGNN and write intermediate dataframes.
- `model_training/`: Uses the combined dataframe to train the surrogate models and store the resulting `*.joblib` files and grid-search results.
- `model_backend/`: Instructions and helper scripts to build and run the Docker images for the Embedded-Kittens and surrogate-model backend services.
- `results/`: Jupyter notebooks and data used to (re-)generate the thesis tables and figures from raw or pre-aggregated experiment outputs.
- `temp_results/`: Local placeholder for raw experiment logs copied from the Whisker cluster experiments.

For details about each step and folder, see the corresponding `README.md` files.