import argparse
import sys
from pathlib import Path
from time import time

sys.path.append(str(Path(__file__).parent))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--version",
        help="print version of this package",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--language-version",
        help="prints version of the tree-sitter-python-language that is being compiled",
        action="store_true",
        default=False,
    )

    return parser.parse_args()


def main():
    args = parse_args()
    if args.version:
        from _versions import __version__

        print(__version__)

    elif args.language_version:
        from _versions import __grammar_version__

        print(__grammar_version__)

    else:
        start = time()
        from _build import py_language

        py_language(rebuild=True)
        print(f"Recompiled language in {time() - start:0.4} seconds")


if __name__ == "__main__":
    main()
