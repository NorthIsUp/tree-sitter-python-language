import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from tree_sitter_python_language import (build_python_language,
                                         download_and_extract_language_zip)

download_and_extract_language_zip()
build_python_language()
