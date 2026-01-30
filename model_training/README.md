# Model training

This folder contains everything needed to train the surrogate models used in the experiments.

## Inputs

- `df.pickle`: Combined dataframe created by the scripts in `variants_out/`.
	- Each row corresponds to a program variant.
	- Contains GGNN-based program embeddings (`project*` columns) and the corresponding repair outcomes (e.g., `fitness`, test outcome indicators).

## Structure

- `fitness/training.py`
	- Trains a regression model (MLPRegressor) to predict the fitness value of a variant.
	- Reads `../df.pickle`.
	- Performs a grid search over MLP hyperparameters.
	- Writes:
		- `grid_search_results.csv` (all evaluated hyperparameters and scores)
		- `mlp_best.joblib` (best model, scaler, and metadata)

- `testoutcome/training.py`
	- Trains a multi-label classifier (MLPClassifier) to predict test outcomes for each test case.
	- Reads `../df.pickle`.
	- Performs a grid search over MLP hyperparameters with an F1-micro objective.
	- Writes:
		- `grid_search_results.csv` (all evaluated hyperparameters and scores)
		- `mlp_classifier_best.joblib` (best model, scaler, and metadata)

- `analysis/` and `mlp_best_handling.ipynb`
	- Optional notebooks for inspecting training behaviour and the resulting models.
	- Not strictly required to reproduce the main experimental results.

## How to train the models

1. Ensure `df.pickle` is present in this directory (created by `variants_out/04_combineFruitCatchingDfs.py`).
2. Activate the replication environment (see `environment/README.md`).
3. Train the fitness model locally:
	 ```bash
	 cd model_training/fitness
	 python training.py
	 ```
4. Train the test-outcome model locally:
	 ```bash
	 cd ../testoutcome
	 python training.py
	 ```

### Running training on the cluster

If you are using the original SLURM-based cluster setup, you can instead submit the provided shell scripts:

- From `model_training/fitness/`:
	 ```bash
	 sbatch training.sh
	 ```
- From `model_training/testoutcome/`:
	 ```bash
	 sbatch training.sh
	 ```

These scripts contain cluster-specific paths and environment variables; adapt them to your own cluster configuration if needed.

After these steps (either local or cluster training), the files `mlp_best.joblib` and `mlp_classifier_best.joblib` are ready to be copied into the backend repository (`bauers-ma/backend/files/trained_model/`) as described in `model_backend/README.md`.