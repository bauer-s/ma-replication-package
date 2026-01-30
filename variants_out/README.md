# Variants Out Directory

In this folder, the variants from the `variants` folder are processed and combined with program embeddings to create the dataframe used for model training.

## Overview

- Input:
	- Variants and `results.csv` in `../variants/` (see `variants/README.md`).
	- Program-embedding configuration in `environment/programEmbeddingConfig/`.
- Output:
	- Intermediate pickles under `games/fruit_catching/`.
	- Final combined dataframe `../model_training/df.pickle`.

## Scripts and notebooks

- `01_findFoldersWithFruitCatchingProjects.ipynb`
	- Helper notebook to identify folders that contain FruitCatching projects.
	- Optional for replication; the mapping can also be provided manually via `games/FruitCatching.txt`.

- `02_resultsCsvToDf.py`
	- Reads `../variants/results.csv`.
	- Filters rows for the selected project(s) (e.g., FruitCatching).
	- Cleans and deduplicates the data.
	- Writes the aggregated dataframe to `results.pickle` in this directory.

- `03_combineResultsWithModelInput.py`
	- Prerequisites:
		- The Embedded-Kittens microservice is running and reachable from this machine.
		- The GGNN embedding tool is available via the configuration in `environment/programEmbeddingConfig/model-config.yaml`.
		- `results.pickle` has been created by `02_resultsCsvToDf.py`.
	- For each variant JSON/JSONL file listed in `games/FruitCatching.txt`:
		- Calls Embedded-Kittens to normalise/convert the program representation.
		- Runs the GGNN embedding tool to obtain a numeric embedding.
		- Merges the embedding with the corresponding row in `results.pickle`.
	- Writes one dataframe per folder to `games/fruit_catching/df_<folder>.pickle`.

- `04_combineFruitCatchingDfs.py`
	- Reads all `df_*.pickle` files from `games/fruit_catching/`.
	- Checks that the number of rows matches the number of variant files per folder.
	- Concatenates the dataframes, removes duplicates and missing values.
	- Writes the final combined dataframe to `../model_training/df.pickle`.

## Run order

1. Prepare `variants/` (variants and `results.csv`).
2. Run `02_resultsCsvToDf.py` to create `results.pickle`.
3. Ensure Embedded-Kittens and the GGNN environment are running and accessible.
4. Run `03_combineResultsWithModelInput.py` to generate the per-folder pickles in `games/fruit_catching/`.
5. Run `04_combineFruitCatchingDfs.py` to create `../model_training/df.pickle`.

Note: The URL of the Embedded-Kittens service is configured inside `03_combineResultsWithModelInput.py`. Adjust it if you deploy the service under a different host or port.