import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from _build import py_language

py_language(rebuild=True)
