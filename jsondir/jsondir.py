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


def resolve_name(path):
    """Resolves the name of the given path.

    When using path.name to get the name of a file, pathlib returns an
    empty string for cwd and root. To get around this, we need to
    specify the proper names ourselves.

    Parameters
    ----------
    path : pathlib.Path object
        The path to resolve the name for.

    Returns
    -------
    name : string
        The resolved file name.

    """

    abspath = str(path.resolve())
    if abspath == "/":
        name = "/"
    elif abspath == str(pathlib.Path.cwd()):
        name = "."
    else:
        name = path.name

    return name


def print_file(path, indent_level):
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

    name = path.name
    if not name:
        name = resolve_name(path)

    name_str = "\"name\": \"{}\"".format(name)
    output_strings.append(name_str)

    if path.is_symlink():
        target_str = "\"target\": \"{}\"".format(path.resolve())
        output_strings.append(target_str)

    for info_str in output_strings:
        if info_str == output_strings[-1]:
            print(" " * TAB_SIZE * indent_level + info_str)
        else:
            print(" " * TAB_SIZE * indent_level + info_str + ",")



def print_directory(path, indent_level,  show_hidden=False):
    """Display information for each file in the given directory.
    
    Parameters
    ----------
    path : pathlib.Path object
        The directory to show information for.

    indent_level : int
        Number of tabs to insert before printing strings.
        Note that this is for the braces; the file information
        will be indented one level deeper.

    show_hidden : bool
        Whether to include files whose names start with "."

    """

    if show_hidden:
        children = [child for child in path.iterdir()]
    else:
        children = [child for child in path.iterdir() if not child.name.startswith('.')]

    children.sort(key=lambda child: child.name.lower().strip('.'))

    print(" " * TAB_SIZE * indent_level + "{")
    print_file(path, indent_level + 1)

    print(" " * TAB_SIZE * (indent_level + 1) + "\"children\": [")

    for child in children:
        print(" " * TAB_SIZE * (indent_level + 2) + "{")
        print_file(child, indent_level + 3)

        if child == children[-1]:
            print(" " * TAB_SIZE * (indent_level + 2) + "}")
        else:
            print(" " * TAB_SIZE * (indent_level + 2) + "},")

    print(" " * TAB_SIZE * (indent_level + 1) + "]")

    print(" " * TAB_SIZE * indent_level + "}")

def main():
    args = process_args()

    for filename in args.files:
        path = pathlib.Path(filename)

        try:
            if path.is_dir():
                print_directory(path, 0, args.all)
            else:
                print_file(path, 0)
        except FileNotFoundError:
            print("{}: No such file or directory.".format(filename))


if __name__ == "__main__":
    main()
