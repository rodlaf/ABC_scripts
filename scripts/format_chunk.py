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

TOPLEVEL_DIR = "/root/ABC_scripts"
BASH_SCRIPTS_DIR = f"{TOPLEVEL_DIR}/scripts"
LOG_DIR = f"{TOPLEVEL_DIR}/logs"
DATASET_DIR = f"{TOPLEVEL_DIR}/dataset"


def process_yaml_file(filename: str, meta_dir_path: str, db_name: str) -> None:
    conn = sqlite3.connect(db_name)

    with open(os.path.join(meta_dir_path, filename), "r") as yaml_file:
        # Attempt attainment of name and id
        try: 
            meta_json: dict = yaml.safe_load(yaml_file)
            
            name: str = meta_json['name']
            file_num: int = int(filename[:8])
        except:
            print('Error processing ', filename)
            conn.close()
            return
        
        # Insert into db
        cur = conn.cursor()
        query = Query.into(Table('meta')).insert(file_num, name)
        cur.execute(str(query))
        conn.commit()

    conn.close()


def main(args: argparse.Namespace) -> None:
    db_name = f'chunk_{args.chunk_num}.db'

    # Delete and reopen db, create table
    if os.path.exists(db_name):
        os.remove(db_name)
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    # cur.execute('pragma journal_mode=wal') # Use write-ahead logging
    query = Query.create_table('meta').columns(
        Column('file_num', "INT"),
        Column('name', 'TEXT'),
    )
    cur.execute(str(query))
    conn.commit()
    conn.close()

    # Get list of yaml file names
    meta_dir_path = os.path.join(DATASET_DIR, f"meta_extracted_{str(args.chunk_num)}")
    yaml_file_list = os.listdir(meta_dir_path)

    start = time.time()

    if args.parallel == 1:
        print("Using parallelization.")

        unary = partial(
            process_yaml_file,
            meta_dir_path=meta_dir_path,
            db_name=db_name
        )

        # Give each process one file to process.
        with Pool() as pool:
            for _ in tqdm(
                pool.imap(unary, yaml_file_list, chunksize=64),
                total=len(yaml_file_list),
            ):
                pass

    else:
        print("Not using parallelization.")

        for filename in tqdm(yaml_file_list):
            process_yaml_file(filename, meta_dir_path, db_name)

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
        default=1
    )

    return parser.parse_args()


if __name__ == "__main__":
    main(args=parse_args())
