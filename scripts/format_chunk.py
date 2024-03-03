import argparse
import time
import os
from tqdm import tqdm
from multiprocessing import Pool
import time
from functools import partial
import yaml

TOPLEVEL_DIR = "/root/ABC_scripts"
BASH_SCRIPTS_DIR = f"{TOPLEVEL_DIR}/scripts"
LOG_DIR = f"{TOPLEVEL_DIR}/logs"
DATASET_DIR = f"{TOPLEVEL_DIR}/dataset"


def process_yaml_file(filename: str, meta_dir_path: str, output_file_path: str) -> None:
    with open(os.path.join(meta_dir_path, filename), "r") as yaml_file:
        meta_json: dict = yaml.safe_load(yaml_file)

        with open(os.path.join(os.getcwd(), output_file_path), "a") as output_file:
            output_file.write(str(meta_json))


def main(args: argparse.Namespace) -> None:
    meta_dir_path = os.path.join(DATASET_DIR, f"meta_extracted_{str(args.chunk_num)}")
    output_file_path = "output.txt"

    if os.path.exists(output_file_path):
        os.remove(output_file_path)
    open(output_file_path, "w")

    start = time.time()

    if args.parallel == 1:
        print("Using parallelization.")

        unary = partial(
            process_yaml_file,
            meta_dir_path=meta_dir_path,
            output_file_path=output_file_path,
        )
        filename_list = os.listdir(meta_dir_path)

        with Pool() as pool:
            for _ in tqdm(
                pool.imap_unordered(unary, filename_list, chunksize=1),
                total=len(filename_list),
            ):
                pass

    else:
        print("Not using parallelization.")

        for filename in tqdm(os.listdir(meta_dir_path)):
            process_yaml_file(filename, meta_dir_path, output_file_path)

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
        help="Whether or not to use parallelization. 0 or 1",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main(args=parse_args())
