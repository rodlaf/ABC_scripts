
filenames = []

TOPLEVEL_DIR = "/root/ABC_scripts"
DATASET_DIR = f"{TOPLEVEL_DIR}/dataset"

for i in range(0, 99):
    filenames.append(f"{DATASET_DIR}/data_{i}.jsonl")

with open('data.jsonl', 'w') as outfile:
    for fname in filenames:
        try:
            with open(fname) as infile:
                outfile.write(infile.read())
        except:
            print(fname)
