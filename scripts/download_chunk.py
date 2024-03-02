import argparse
import shlex, subprocess
import time

TOPLEVEL_DIR = "/root/ABC_scripts"
BASH_SCRIPTS_DIR = f"{TOPLEVEL_DIR}/scripts"
LOG_DIR = f"{TOPLEVEL_DIR}/logs"


# TODO: Finish path setting functionality (can set default)
def main(args: argparse.Namespace) -> None:
    chunk_num = args.chunk_num
    log_path = f"{LOG_DIR}/download_{int(time.time())}.log"

    p = subprocess.Popen(
        ["nohup", f"{BASH_SCRIPTS_DIR}/b_download_chunk.sh", str(chunk_num)],
        stdout=open(log_path, "w"),
        stderr=subprocess.STDOUT,
    )

    print(
        f"""
    Download output is located at {args.dataset_path}.
    Logging of this job is located at `{log_path}`.
    Run `pkill -P {p.pid}` in order to kill this job.
    """
    )


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
        required=True,
        help="Number of chunk to download and extract. Must be in [0, 99].",
    )

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    main(args=parse_args())
