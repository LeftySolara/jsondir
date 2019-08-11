import argparse
import stat
import pathlib
from enum import Enum, unique, auto


TAB_SIZE = 4


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


TYPE_STRINGS = {
    FileType.DIR: "directory",
    FileType.REG: "regular file",
    FileType.LNK: "symbolic link",
    FileType.SOCK: "socket",
    FileType.FIFO: "named pipe",
    FileType.BLK: "block device file",
    FileType.CHR: "character special device file",
    FileType.UNKNOWN: "unknown"
}


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


def print_file(path, tab_count):
    """Display information for a single file.

    Parameters
    ----------
    path : pathlib.Path
        The path to display information for.

    tab_count : int
        Number of tabs to insert for indentation.

    """

    output_strings = []

    file_type = FileType.get_file_type(path)
    type_str = "\"type\": \"{}\"".format(TYPE_STRINGS[file_type])
    output_strings.append(type_str)

    # For root and cwd, path.name returns an empty string.
    # Thus, we need to manually enter the correct values.
    abspath = str(path.resolve())
    if abspath == "/":
        name = "/"
    elif abspath == str(pathlib.Path.cwd()):
        name = "."
    else:
        name = path.name

    name_str = "\"name\": \"{}\"".format(name)
    output_strings.append(name_str)

    if path.is_symlink():
        target_str = "\"target\": \"{}\"".format(path.resolve())
        output_strings.append(target_str)

    for info_str in output_strings:
        print(" " * TAB_SIZE * tab_count + info_str)


def main():
    args = process_args()

    for filename in args.files:
        try:
            path = pathlib.Path(filename)
            print()
            print_file(path, 0)
        except FileNotFoundError:
            print("{}: No such file or directory.".format(filename))

if __name__ == "__main__":
    main()

