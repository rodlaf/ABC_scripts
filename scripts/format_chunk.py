import argparse
import time
import os
from tqdm import tqdm
from multiprocessing import Pool
import time
from functools import partial

TOPLEVEL_DIR = "/root/ABC_scripts"
BASH_SCRIPTS_DIR = f"{TOPLEVEL_DIR}/scripts"
LOG_DIR = f"{TOPLEVEL_DIR}/logs"
DATASET_DIR = f"{TOPLEVEL_DIR}/dataset"


def write_line_36(filename: str, meta_dir_path: str) -> None:
    with open(os.path.join(meta_dir_path, filename), "r") as f:
        content = f.readlines()
        with open(os.path.join(os.getcwd(), "output.txt"), "a") as f2:
            f2.write(content[36])


def main(args: argparse.Namespace) -> None:
    meta_dir_path = os.path.join(DATASET_DIR, f"meta_extracted_{str(args.chunk_num)}")

    start = time.time()

    if args.parallel == 1:
        print("Using parallelization.")

        unary = partial(write_line_36, meta_dir_path=meta_dir_path)
        filename_list = os.listdir(meta_dir_path)

        with Pool() as pool:
            for _ in tqdm(
                pool.imap_unordered(unary, filename_list, chunksize=512),
                total=len(filename_list),
            ):
                pass

    else:
        print("Not using parallelization.")

        for filename in tqdm(os.listdir(meta_dir_path)):
            write_line_36(filename, meta_dir_path)

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
