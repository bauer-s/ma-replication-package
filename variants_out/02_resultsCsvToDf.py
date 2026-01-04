import pandas as pd


file_name_df = "results.pickle"
print("File name df:", file_name_df)

DTYPES = {
    #"iteration": "uint16",
    "hashCode": "int",
    #"viable": "bool",
    #"reason": "category",
    #"length": "uint16",
    #"initial": "bool",
    "fitness": "float",
    #"numPass": "int8",
    #"numFail": "int8",
    #"newlyNumPass": "int8",
    #"newlyNumFail": "int8",
    #"coverage": "float",
    "passing": "object",
    "failing": "object",
    #"runTests": "uint32",
    #"now": "uint32",
    #"job_id": "uint16",
    #"rep": "uint8",
    #"config": "category",
    "project": "category",
    #"test": "category",
}

# Should lead to 62 iterations
chunksize = 10 ** 6

# TODO: Change rootdir to variants
# rootdir = Path.cwd().parent / "variants"
rootdir = '/scratch/bauers/variants'
file_path = rootdir + "/results.csv"

reader = pd.read_csv(file_path, usecols=DTYPES.keys(), dtype=DTYPES,chunksize=chunksize)



li = []
for i, chunk in enumerate(reader):
    print(f"Iteration {i+1}")
    temp_df = chunk[chunk['project'].str.match('FruitCatching*')]
    temp_df.reset_index(drop=True,inplace=True)

    li.append(temp_df)

df = pd.concat(li, axis=0, ignore_index=True)

print("Shape", df.shape)


def get_test_names(row):
    test_names = sorted(row["passing"].split(";"))

    print("Len Test names: ", len(test_names))
    print("Test names: ", test_names)
    return test_names

test_names = get_test_names(df.sort_values(by="fitness", ascending=False).iloc[0])
for test_name in test_names:
    print("Processing test name:", test_name)
    df[test_name] = df.passing.str.contains(test_name)

df.reset_index(inplace=True)
df = df.drop_duplicates('hashCode', keep='last')

print("Shape wo duplicates", df.shape)

df = df[df.notna().all(axis=1)]
print("Shape wo nan", df.shape)

df.to_pickle(file_name_df)