import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from _build import fetch_and_build_python_language

fetch_and_build_python_language()
