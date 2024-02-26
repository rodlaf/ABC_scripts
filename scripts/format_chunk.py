import argparse
import shlex, subprocess
import time
import os
from tqdm import tqdm

TOPLEVEL_DIR = "/workspace/ABC_scripts"
BASH_SCRIPTS_DIR = f"{TOPLEVEL_DIR}/scripts"
LOG_DIR = f"{TOPLEVEL_DIR}/logs"


def main(args: argparse.Namespace) -> None:
    meta_dir_path = os.path.join(
        args.dataset_path, f"meta_extracted_{str(args.chunk_num)}"
    )

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
        "--dataset_path",
        type=str,
        required=True,
        help="Path to download and extract chunk into",
    )
    parser.add_argument(
        "--chunk_num",
        type=int,
        required=True,
        help="Number of chunk to download and extract. Must be in [0, 99].",
    )

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    main(args=parse_args())
