import argparse
import shlex, subprocess 

# This is where this script will look for the bash scripts it needs
BASH_SCRIPTS_DIR = "/workspace/ABC_scripts/scripts"


def main(args: argparse.Namespace) -> None:
    p = subprocess.Popen([f'{BASH_SCRIPTS_DIR}/test_script.sh'])

    print(f"""
        Download output is stored in 
        Run `pkill -9 {p.pid}` in order to kill this job.
    """)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="""
            Download and extract a specific chunk of the ABC dataset.
            Will extract meta and step files.
            A process will be spawned and all output will be recorded in an log file.
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
        help="Number of chunk to download and extract. Must be in [0, 99].",
    )

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    main(args=parse_args)
