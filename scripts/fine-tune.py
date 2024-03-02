import argparse
import subprocess
import time
import os
from tqdm import tqdm

TOPLEVEL_DIR = "/root/ABC_scripts"
BASH_SCRIPTS_DIR = f"{TOPLEVEL_DIR}/scripts"
LOG_DIR = f"{TOPLEVEL_DIR}/logs"
DATASET_DIR = f"{TOPLEVEL_DIR}/dataset"


def main(args: argparse.Namespace) -> None:
    meta_dir_path = os.path.join(DATASET_DIR, f"meta_extracted_{str(args.chunk_num)}")

    for filename in tqdm(os.listdir(meta_dir_path)):
        with open(os.path.join(meta_dir_path, filename), "r") as f:
            content = f.readlines()
            with open(os.path.join(os.getcwd(), "output.txt"), "a") as f2:
                f2.write(content[36])


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
        help="Number of chunk to fine-tune on. Must be in [0, 99].",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main(args=parse_args())
