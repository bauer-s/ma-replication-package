# Thesis results analysis (replication notebooks)

This folder contains the notebooks used to (re-)generate the tables/figures that the thesis includes.

**Folders**
- `raw_data/`: aggregated CSV inputs (generated from raw experiment logs)
- `data/`: generated thesis artifacts (LaTeX tables + PDF/PNG figures). This folder is the canonical output for the replication package.

## Quick start (recommended run order)

1) Ensure the raw experiment logs are present under `temp_results/`:
   - `temp_results/baseline/`
   - `temp_results/surrogate-model/`

2) Generate aggregated CSV inputs:
   - Run the raw-data creation notebook:
      - `03_create_raw_data.ipynb`
   - Outputs: `raw_data/*.csv`

3) Generate the repair-analysis thesis assets:
   - Run `04_analyze_repair_results_thesis_assets.ipynb`
   - Outputs (in `data/`):
     - `latex_table_time_efficiency.tex`
     - `latex_table_statistical_tests.tex`
     - `figure_repair_duration_distribution.pdf/png`
     - `figure_stopping_conditions.pdf/png`
     - `figure_generations_completed.pdf/png`

4) (Optional) Extended analysis / exploration:
    - Use `01_analyze_training_data.ipynb` for additional plots and statistics based on the model-training results.

5) (Optional) Generate the hyperparameter top-10 tables:
    - Run `02_create_hyperparameter_tables.ipynb`
    - Inputs required (produced by the model training step, not by step 2):
       - `../model_training/fitness/grid_search_results.csv`
       - `../model_training/testoutcome/grid_search_results.csv`
    - Outputs (in `data/`):
       - `fitness_top10_hyperparameters.tex` (+ `.csv`)
       - `testoutcome_top10_hyperparameters.tex` (+ `.csv`)


