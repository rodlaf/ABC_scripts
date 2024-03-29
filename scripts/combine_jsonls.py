filenames = []

TOPLEVEL_DIR = "/root/ABC_scripts"
DATASET_DIR = f"{TOPLEVEL_DIR}/dataset"

for i in range(0, 99):
    filenames.append(f"{DATASET_DIR}/data_{i}.jsonl")

with open("data.jsonl", "w") as outfile:
    for fname in filenames:
        try:
            with open(fname) as infile:
                file_string: str = infile.read()
                file_string = file_string.replace('{"instruction":', '\n{"instruction":')
                outfile.write(file_string)
        except:
            print(fname)
