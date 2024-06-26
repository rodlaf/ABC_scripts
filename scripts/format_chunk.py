import argparse
import time
import os
from tqdm import tqdm
from multiprocessing import Pool
import time
from functools import partial
import yaml
import sqlite3
from pypika import Query, Table, Column
import fcntl
import json

# TOPLEVEL_DIR = "/root/ABC_scripts"
TOPLEVEL_DIR = "/home/rslm/ABC_scripts"

BASH_SCRIPTS_DIR = f"{TOPLEVEL_DIR}/scripts"
LOG_DIR = f"{TOPLEVEL_DIR}/logs"
DATASET_DIR = f"{TOPLEVEL_DIR}/dataset"
PROCESSED_DATASET_DIR = f"{TOPLEVEL_DIR}/processed_dataset"
DB_DIR = f"{TOPLEVEL_DIR}/processed_dataset_dbs"

MAX_STEP_FILE_SIZE = 32000
INSTRUCTION = """
You are SplineGPT. You create CAD models from text. You will be given a short blurb of 
words as a prompt and you must generate a valid .STEP file for which the prompt is a 
valid description.
"""


def process_data_point(
    step_meta_tuple: tuple[str, str],
    step_dir_path: str,
    meta_dir_path: str,
    db_name: str,
    data_jsonl_path: str,
) -> None:
    step_filename, meta_filename = step_meta_tuple
    step_file_path = os.path.join(step_dir_path, step_filename)
    step_file_id = int(step_filename[:8])
    meta_file_path = os.path.join(meta_dir_path, meta_filename)
    meta_file_id = int(meta_filename[:8])
    assert step_file_id == meta_file_id

    # step file stats
    step_file_stats = os.stat(step_file_path)
    step_file_size = step_file_stats.st_size
    if step_file_size > MAX_STEP_FILE_SIZE:
        return

    # Attempt attainment of name from meta
    name = None
    with open(meta_file_path, "r") as yaml_file:
        try:
            meta_json: dict = yaml.safe_load(yaml_file)
            name: str = meta_json["name"]
        except:
            print("Error processing ", meta_filename, ".")
            return

    # Insert info into db
    conn = sqlite3.connect(db_name)
    try:
        cur = conn.cursor()
        query = Query.into(Table("meta")).insert(step_file_id, name)
        cur.execute(str(query))
        conn.commit()
    # duplicate names will fail
    except:
        conn.close()
        return
    conn.close()

    step_file_string = None
    with open(step_file_path, "r") as file:
        step_file_string = file.read().replace("\n", "")

    # put into .jsonl
    data_point_dict = {
        "instruction": INSTRUCTION,
        "input": name,
        "output": step_file_string,
    }

    new_entry = json.dumps(data_point_dict)

    with open(data_jsonl_path, "a") as g:
        fcntl.flock(g, fcntl.LOCK_EX)
        g.write('\n' + new_entry)
        fcntl.flock(g, fcntl.LOCK_UN)


def main(args: argparse.Namespace) -> None:
    db_name = os.path.join(DB_DIR, f"chunk_{args.chunk_num}.db")

    data_jsonl_path = f"{PROCESSED_DATASET_DIR}/data_{args.chunk_num}.jsonl"

    # Delete and reopen db, create table
    if os.path.exists(db_name):
        os.remove(db_name)
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    # cur.execute('pragma journal_mode=wal') # Use write-ahead logging
    query = Query.create_table("meta").columns(
        Column("file_id", "INT"),
        Column("name", "TEXT UNIQUE"),
    )
    cur.execute(str(query))
    conn.commit()
    conn.close()

    # zip meta and step file paths
    step_dir_path = os.path.join(DATASET_DIR, f"step_extracted_{str(args.chunk_num)}")
    step_file_list = sorted(os.listdir(step_dir_path))
    meta_dir_path = os.path.join(DATASET_DIR, f"meta_extracted_{str(args.chunk_num)}")
    meta_file_list = sorted(os.listdir(meta_dir_path))
    step_meta_tuples = list(zip(step_file_list, meta_file_list))

    start = time.time()

    if args.parallel == 1:
        print("Using parallelization.")

        unary = partial(
            process_data_point,
            step_dir_path=step_dir_path,
            meta_dir_path=meta_dir_path,
            db_name=db_name,
            data_jsonl_path=data_jsonl_path,
        )

        # Give each process one file to process.
        with Pool() as pool:
            for _ in tqdm(
                pool.imap(unary, step_meta_tuples, chunksize=64),
                total=len(step_meta_tuples),
            ):
                pass

    else:
        print("Not using parallelization.")

        for step_meta_tuple in tqdm(step_meta_tuples):
            process_data_point(
                step_meta_tuple=step_meta_tuple,
                step_dir_path=step_dir_path,
                meta_dir_path=meta_dir_path,
                db_name=db_name,
                data_jsonl_path=data_jsonl_path,
            )

    end = time.time()
    print("Elapsed time: ", end - start)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="""
        Format directory of ABC chunk into usable finetuning data.
        """
    )

    parser.add_argument(
        "--chunk_num",
        type=int,
        required=True,
        help="Number of chunk to download and extract. Must be in [0, 99].",
    )
    parser.add_argument(
        "--parallel",
        type=int,
        help="Whether or not to use parallelization. 0 or 1. Default is 1.",
        default=1,
    )

    return parser.parse_args()


if __name__ == "__main__":
    main(args=parse_args())
