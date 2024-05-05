import json
import tqdm

MAX_STEP_FILE_LEN = 16000

outfile = open("/root/ABC_scripts/small_data.jsonl", "a")
with open("/root/ABC_scripts/data.jsonl", "r") as infile:
    for line in tqdm.tqdm(infile):
        obj = json.loads(line)
        step_file = obj['output']
        if len(step_file) <= MAX_STEP_FILE_LEN:
            outfile.write(line)