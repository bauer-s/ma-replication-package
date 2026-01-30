# Variants Folder

Place all already generated variants in this folder. These variants are the per-job outputs produced by the Whisker repair runs.

The folder structure should look like this:

- 1
  - `BoatRace-1--132895.json`
  - ...
- 2
- ...
- `results.csv`

Here, `results.csv` is the global summary file exported by Whisker (one row per variant). The scripts in `variants_out/` assume this layout and use `results.csv` together with the per-folder JSON/JSONL files to build the training dataframe.