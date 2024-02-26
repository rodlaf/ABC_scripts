import argparse
import shlex, subprocess
import time

TOPLEVEL_DIR = "/workspace/ABC_scripts"
BASH_SCRIPTS_DIR = f"{TOPLEVEL_DIR}/scripts"
LOG_DIR = f"{TOPLEVEL_DIR}/logs"


def main(args: argparse.Namespace) -> None:
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="""
        Format directory of ABC chunk into usable finetuning data.
        """
    )

    parser.add_argument(
        "--dataset_path",
        type=str,
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
