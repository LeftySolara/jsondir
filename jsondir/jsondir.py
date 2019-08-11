import argparse
import stat
import pathlib
from enum import Enum, unique, auto


@unique
class FileType(Enum):
    """Unix file types"""

    DIR = 0        # Directory
    REG = auto()   # Regular file
    LNK = auto()   # Symbolic link
    SOCK = auto()  # Socket
    FIFO = auto()  # Named pipe
    BLK = auto()   # Block device file
    CHR = auto()   # Character special device file
    UNKNOWN = auto()   # Unknown

    # https://stackoverflow.com/questions/44595736/get-unix-file-type-with-python-os-module
    @classmethod
    def get_file_type(cls, path):
        """Get the file type of the given path."""
        if not isinstance(path, int):
            path = path.lstat().st_mode
        for path_type in cls:
            method = getattr(stat, 'S_IS' + path_type.name.upper())
            if method and method(path):
                return path_type
        return cls.UNKNOWN


def process_args():
    """
    Specify and parse command line arguments.

    Returns
    -------
    namespace : argparse.Namespace
        Populated namespace containing argument attributes.

    """

    parser = argparse.ArgumentParser(
        prog="jsondir",
        description="Display directory structure in JSON format" \
            " or create directory structure from JSON file.",
        usage="%(prog)s [OPTION]... [FILE]..."
    )

    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        required=False,
        help="include all files, including hidden ones"
    )

    parser.add_argument(
        "files",
        nargs="*",
        default=".",
        type=str,
        metavar="FILES",
        help="the files or directories to display"
    )

    namespace = parser.parse_args()
    return namespace


def main():
    args = process_args()

    if args.all:
        print("--all flag passed")

    print(args.files)


if __name__ == "__main__":
    main()

