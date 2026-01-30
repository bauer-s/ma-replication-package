import os
from pathlib import Path

import pandas as pd

dir_dfs = Path(__file__).resolve().parent / "games" / "fruit_catching"

# Use the repository-local variants directory instead of a cluster-specific path
dir_in = Path(__file__).resolve().parents[1] / "variants"

# Output combined dataframe
df_out_name = Path(__file__).resolve().parents[1] / "model_training" / "df.pickle"


dfs = []

len_should = 0
len_should_clean = 0

with os.scandir(dir_dfs) as it:
    for entry in it:
        if entry.name.endswith(".pickle"):
            df = pd.read_pickle(entry.path)

            folder_name = entry.name.removesuffix(".pickle").removeprefix("df_")
            len_files = len(os.listdir(dir_in / folder_name))
            len_df = df.shape[0]


            df.drop(['index', 'passing', 'failing'], axis=1, inplace=True, errors='ignore')

            df.dropna(inplace=True)
            df.reset_index(inplace=True, drop=True)
            
            len_df_clean = df.shape[0]
            
            print(f"Processing '{folder_name}' (Complete: {len_files == len_df_clean}) with {len_files} files and {len_df} (len_df_clean: {len_df_clean}) rows")
            dfs.append(df)

            len_should += len_files
            len_should_clean += len_df_clean

assert len(dfs) == 246

df = pd.concat(dfs)
print("Shape", df.shape)


print("Shape after drop columns", df.shape)

df.drop_duplicates(subset=['hashCode'], inplace=True)
df.reset_index(inplace=True, drop=True)
print("Shape wo duplicates", df.shape)


df.dropna(inplace=True)
print("Shape wo na", df.shape)

print("Len should:", len_should)
print("Len should clean:", len_should_clean)




df.to_pickle(df_out_name)