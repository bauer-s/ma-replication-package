## Replication Package – Environment Setup

This project uses a Conda virtual environment to ensure reproducibility.

### Requirements
- Miniconda or Anaconda installed
- Conda ≥ 23.x

### Environment Setup

1. Navigate to the `environment/` directory:
   ```bash
   cd environment
   ```
2. Create the Conda environment:
   ```bash
   conda env create -f environment.yml
   ```

3. Activate the environment:
   ```bash
   conda activate ggnn-env
   ```

4. Install pip dependencies:
   ```bash
   pip install -r requirements.txt
   ```