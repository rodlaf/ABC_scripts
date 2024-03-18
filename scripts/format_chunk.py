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

import sys

FREECAD_PATH = "/usr/lib/freecad-python3/lib"
sys.path.append(FREECAD_PATH)
import FreeCAD  # type: ignore
import Import  # type: ignore

TOPLEVEL_DIR = "/root/ABC_scripts"
BASH_SCRIPTS_DIR = f"{TOPLEVEL_DIR}/scripts"
LOG_DIR = f"{TOPLEVEL_DIR}/logs"
DATASET_DIR = f"{TOPLEVEL_DIR}/dataset"

MAX_STEP_FILE_SIZE = 16000


def process_yaml_file(
    step_meta_tuple, # TODO
    step_dir_path: str,
    meta_dir_path: str, 
    db_name: str,
) -> None:
    conn = sqlite3.connect(db_name)

    step_filename, meta_filename = step_meta_tuple

    step_file_path = os.path.join(step_dir_path, step_filename)
    step_file_id = int(step_filename[:8])

    meta_file_path = os.path.join(meta_dir_path, meta_filename)
    meta_file_id = int(meta_filename[:8])

    assert(step_file_id == meta_file_id)
    file_id = step_file_id

    # Attempt attainment of name from meta
    name = None
    with open(meta_file_path, "r") as yaml_file:
        try:
            meta_json: dict = yaml.safe_load(yaml_file)
            name: str = meta_json["name"]
        except:
            print("Error processing ", meta_filename, ".")
            conn.close()
            return

    # step file stats
    step_file_stats = os.stat(step_file_path)
    step_file_size = step_file_stats.st_size
    step_file_size_kilobytes = round(step_file_stats.st_size / (1024), 1)

    ############# FreeCAD stuff #############
    # # initialize FreeCAD
    # doc = FreeCAD.newDocument()
    # FreeCAD.setActiveDocument(doc.Name)

    # # import step file
    # Import.insert(step_file_path, doc.Name)

    # # if len(doc.Objects) > 1:
    # # print(f"ID: {step_file_id}, NAME: {name}")
    # for i, obj in enumerate(doc.Objects):
    #     # print(f"   Object label: {obj.Label}")
    #     new_obj_path = f"/root/ABC_scripts/out/{file_id}_{i}.step"
    #     Import.export([obj], new_obj_path)
    #     new_obj_stats = os.stat(new_obj_path)

    #     new_file_size = round(new_obj_stats.st_size / (1024), 1)
    #     if new_file_size > step_file_size:
    #         # print('BIGGER')
    #         pass
    #     else:
    #         print(f"file_id: {file_id}, Old Size: {step_file_size}k, New Size: {new_file_size}k")
    ###########################################

    # Insert into db
    if step_file_size < MAX_STEP_FILE_SIZE:
        try:
            cur = conn.cursor()
            query = Query.into(Table("meta")).insert(step_file_id, name, step_file_size, step_filename)
            cur.execute(str(query))
            conn.commit()
        # duplicate names will fail
        except: 
            pass

    conn.close()


def main(args: argparse.Namespace) -> None:
    db_name = f"chunk_{args.chunk_num}.db"

    # Delete and reopen db, create table
    if os.path.exists(db_name):
        os.remove(db_name)
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    # cur.execute('pragma journal_mode=wal') # Use write-ahead logging
    query = Query.create_table("meta").columns(
        Column("file_id", "INT"),
        Column("name", "TEXT UNIQUE"),
        Column("size", "REAL"),
        Column("step_file_name", "TEXT")
    )
    cur.execute(str(query))
    conn.commit()
    conn.close()

    # TODO: zip meta and step paths
    # Get list of step file names
    step_dir_path = os.path.join(DATASET_DIR, f"step_extracted_{str(args.chunk_num)}")
    step_file_list = sorted(os.listdir(step_dir_path))

    meta_dir_path = os.path.join(DATASET_DIR, f"meta_extracted_{str(args.chunk_num)}")
    meta_file_list = sorted(os.listdir(meta_dir_path))

    step_meta_tuples = list(zip(step_file_list, meta_file_list))

    start = time.time()

    if args.parallel == 1:
        print("Using parallelization.")

        unary = partial(
            process_yaml_file,
            step_dir_path=step_dir_path,
            meta_dir_path=meta_dir_path,
            db_name=db_name,
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

        for filename in tqdm(step_file_list):
            process_yaml_file(filename, step_file_list, db_name)

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
