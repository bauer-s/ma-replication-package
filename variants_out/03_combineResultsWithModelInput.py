'''
The results*.pickle is merged with the encoding of the projects.

Prerequisites:
- Embedding-Kittens microservice must be running.

Steps:
- Embedding-Kittens
- GGNN call
- Merge Encoding with results

Input:
- results*.pickle
- project.json
Output: 
- variants_out/fruit_catching/new/df_{cnt}.pickle foreach number in folder with FruitCatching projects.


Usage:
# Activate virtual environment
#source /home/bauers/.venvs/ggnn/bin/activate

# Run in background 
nohup /scratch/bauers/miniconda3/envs/ggnn-env/bin/python 03_combineResultsWithModelInput.py

# kill 3724514
'''

# General imports
import os
import json
from pathlib import Path

import pandas as pd

# Load GGNN
from ggnn.program_embedding.train import ProgramEmbeddingTool
from ggnn.config import load_config

config_path = Path(__file__).resolve().parents[1] / "environment" / "programEmbeddingConfig" / "model-config.yaml"

config = load_config(config_path, None, eval_only=False)
embedding_tool = ProgramEmbeddingTool(config)



import requests

url = 'http://skadi.fim.uni-passau.de:5002/converter/ggnn'
def embedded_kittens_call(content) -> str:
    r = requests.post(url, json=content)

    if r.status_code != 200:
        raise Exception(f"Error: {r.status_code} - {r.text}")
    return r.content.decode('utf-8')



def merge_with_data(df: pd.DataFrame, df_data: pd.DataFrame)-> pd.DataFrame:
    df_new = df.merge(df_data, on='hashCode', how="left")
    df_new.reset_index(drop=True, inplace=True)
    
    return df_new

#import glob
import shutil

def remove_processed_data(dir: str):
    shutil.rmtree(dir)
    #for f in glob.glob(dir+"*.jsonl"):
    #    os.remove(f)

# Load Data
df_data_file_name = Path(__file__).resolve().parent / "results.pickle"
df_data = pd.read_pickle(df_data_file_name)

df_data.drop(columns=["project", "passing", "failing", "index"], inplace=True)
df_data.reset_index(drop=True, inplace=True)

# Process variants dir: EmbeddedKittens, GGNN, Merge with Data-DataFrame and write df to output folder
def process_variants_dir(variants_dir: str) -> pd.DataFrame:
    rows_list = []
    cnt = variants_dir.split('/')[-1]

    df_out_name = Path(__file__).resolve().parent / "games" / "fruit_catching" / f"df_{cnt}.pickle"
    
    # Create output directory if it doesn't exist
    os.makedirs(df_out_name.parent, exist_ok=True)

    if df_out_name.exists():
        print(f"File {df_out_name} already exists. Skipping processing.")
        return

    # Use the repository-local variants directory instead of a cluster-specific path
    variants_root = Path(__file__).resolve().parents[1] / "variants"
    dir_in = variants_root / cnt

    print("Processing: ", cnt, variants_dir, len(os.listdir(dir_in)))


    with os.scandir(dir_in) as it:
        for entry in it:
            if (entry.name.endswith(".json") or entry.name.endswith(".jsonl")) and entry.is_file():
                splitted = os.path.splitext(entry.name)[0].split('-',2)
                
                hashCode = int(splitted[2])
                if len(splitted) != 3 or splitted[2] != str(hashCode):
                    raise Exception(f'Error by split: {len(splitted) != 3} ; Error cast: {splitted[2] != str(hashCode)} ; by {entry.name}')
                
                dict1 = {"hashCode": hashCode}

                with open(os.path.join(entry.path), "r") as f:
                    content = json.load(f)
                    # EmbeddedKittens
                    content_processed = embedded_kittens_call(content)
                    # GGNN
                    content_project = embedding_tool.embedding(content_processed)
                    dict1["project"] = content_project
                rows_list.append(dict1)
            else:
                raise Exception('Other file type')
    
    df = pd.DataFrame(rows_list)

    # Convert 'Code' (Word Embedding) in single columns
    embedding_size = len(df["project"][0])

    code_columns = [f"project{i}" for i in range(embedding_size)]
    code_df = pd.DataFrame(df["project"].tolist(), columns=code_columns)

    # Combine code columns with original dataframe
    df = pd.concat([code_df, df], axis=1)

    # Drop unnecessary columns
    df.drop(columns=["project"], inplace=True)

    df = merge_with_data(df, df_data)

    print(df.shape[0], len(os.listdir(dir_in)))
    
    df.to_pickle(df_out_name)

    file_dirs_in_folders = Path(__file__).resolve().parent / "games" / "FruitCatching.txt"

with open(file_dirs_in_folders) as file:
    lines = [line.rstrip() for line in file]
    #lines = lines[0:10]
    print(lines)
    
    for line in lines:
        process_variants_dir(line)

    