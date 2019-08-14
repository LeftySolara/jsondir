import argparse
import json
import pathlib
import stat
from enum import Enum, auto, unique


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
    """Specify and parse command line arguments.

    Returns
    -------
    namespace : argparse.Namespace
        Populated namespace containing argument attributes.

    """

    parser = argparse.ArgumentParser(
        prog="jsondir",
        description="Display directory structure in JSON format",
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
        "-d",
        "--depth",
        default=1,
        type=int,
        help="descend only depth directories deep"
    )

    parser.add_argument(
        "-f",
        "--follow-symlinks",
        action="store_true",
        required=False,
        help="follow symlinks like directories"
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


def get_file_info(path):
    """Fetch information about a file.

    Parameters
    ----------
    path : pathlib.Path
        The file to fetch info for.

    Returns
    -------
    info : dict
        Information found about the given file.

    """

    info = {}

    info["name"] = resolve_name(path)
    info["type"] = TYPE_STRINGS[FileType.get_file_type(path)]

    if path.is_symlink():
        info["target"] = str(path.resolve())

    return info


def get_dir_info(path, limit, include_hidden=False, follow_links=False, depth=0):
    """Fetch information about a directory.

    Parameters
    ----------
    path : pathlib.Path
        The directory to fetch info for.

    limit : int
        Maximum recursion depth when getting info for child directories.

    include_hidden : bool
        Whether to include children whose names begin with "."

    follow_links: bool
        Whether to follow symlinks to directories.

    depth : int
        Counter for recursion depth.

    Returns
    -------
    info : dict
        Information found about the given file.

    """

    info = get_file_info(path)

    if not path.is_dir() or depth > limit:
        return info
    if not follow_links and path.is_symlink():
        return info


    if include_hidden:
        children = [child for child in path.iterdir()]
    else:
        children = [child for child in path.iterdir() if not child.name.startswith('.')]

    if children:
        children.sort(key=lambda child: child.name.lower().strip('.'))
        depth += 1
        info["children"] = [get_dir_info(child, limit, include_hidden, follow_links, depth+1)
                            for child in children]

    return info


def main():
    args = process_args()

    for filename in args.files:
        path = pathlib.Path(filename)

        info = get_dir_info(path, args.depth, args.all, args.follow_symlinks)
        print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
