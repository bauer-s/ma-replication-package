# Thesis results analysis (replication notebooks)

This folder contains the notebooks used to (re-)generate the tables/figures that the thesis includes.

**Folders**
- `raw_data/`: aggregated CSV inputs (generated from raw experiment logs)
- `data/`: generated thesis artifacts (LaTeX tables + PDF/PNG figures). This folder is the canonical output for the replication package.

## Quick start (recommended run order)

1) Ensure the raw experiment logs are present under `temp/results/`:
   - `temp/results/baseline/`
   - `temp/results/surrogate-model/`

2) Generate aggregated CSV inputs:
   - Run `create_result_raw_data.ipynb`
   - Outputs: `raw_data/*.csv`

3) Generate the repair-analysis thesis assets:
   - Run `analyze_repair_results_thesis_assets.ipynb`
   - Outputs (in `data/`):
     - `latex_table_time_efficiency.tex`
     - `latex_table_statistical_tests.tex`
     - `figure_repair_duration_distribution.pdf/png`
     - `figure_stopping_conditions.pdf/png`
     - `figure_generations_completed.pdf/png`

4) (Optional) Generate the hyperparameter top-10 tables:
   - Run `create_hyperparameter_tables.ipynb`
   - Inputs required (not produced by step 2):
     - `fitness_new/grid_search_results.csv`
     - `testoutcome_new/grid_search_results.csv`
   - Outputs (in `data/`):
     - `fitness_top10_hyperparameters.tex` (+ `.csv`)
     - `testoutcome_top10_hyperparameters.tex` (+ `.csv`)

5) (Optional) Extended repair analysis:
   - Run `create_repair_results.ipynb`
   - Produces the same core repair-analysis artifacts as step 3, but is kept as a more exploratory/extended notebook.

## Exporting into the thesis folders

All notebooks in this folder write into `data/` by default.

If you want the notebooks to also copy outputs into the thesis folders for convenience:
- Set `EXPORT_TO_THESIS = True` in the respective notebook.
- Tables are copied to `tables/`, figures to `diagram/`.

## Notes

- The thesis itself references assets from `tables/` and `diagram/`.
- `data/` is meant to be byte-identical to those referenced assets (for the replication package).
- PlantUML workflow diagrams are handled separately; see `diagram/README.md`.
