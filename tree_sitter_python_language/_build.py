import shutil
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from typing import Dict, Optional

from tree_sitter import Language

_PACKAGE = Path(__file__).parent

_BUILD_INPUT = _PACKAGE / "vendor" / "tree-sitter-python"
_BUILD_OUTPUT = _PACKAGE / "python-language.so"
_TREE_SITTER_ZIP_URL = (
    "https://github.com/tree-sitter/tree-sitter-python/archive/{ref}.zip"
)


def py_language(cache: Dict[str, Language] = {}) -> Language:
    if not cache:
        output_path = build_python_language(rebuild=False)
        cache["python"] = Language(output_path, "python")

    return cache["python"]


def build_python_language(rebuild: bool = False) -> Path:
    """compile the python language into a useable .so file"""
    assert _BUILD_INPUT.exists(), "the language files must be downloaded"

    if _BUILD_OUTPUT.exists() and rebuild:
        _BUILD_OUTPUT.unlink()

    if not _BUILD_OUTPUT.exists():
        build_successful = Language.build_library(
            str(_BUILD_OUTPUT), [str(_BUILD_INPUT)]
        )
        assert build_successful, "python tree-parser language failed to build"

    return _BUILD_OUTPUT


def fetch_python_language_zip(ref: Optional[str] = None) -> None:
    """
    Download and extract the python language repo
    ref: git ref to download, e.g. 'refs/heads/master' or a git sha
    """
    import zipfile
    from io import BytesIO

    import requests

    url = _TREE_SITTER_ZIP_URL.format(ref=ref or "refs/heads/master")
    response = requests.get(url, allow_redirects=True)

    # extracting the zip file contents but remove the top level dirname
    if _BUILD_INPUT.exists():
        rmtree(_BUILD_INPUT, ignore_errors=True)

    with zipfile.ZipFile(BytesIO(response.content)) as zip:
        extract_to = Path(mkdtemp())
        zip.extractall(extract_to)

    extracted, *extra = list(extract_to.glob("*"))
    assert not extra, "there should only be one dir extracted"

    shutil.move(extracted, _BUILD_INPUT)


def fetch_and_build_python_language(ref: Optional[str] = None) -> Language:
    fetch_python_language_zip(ref=ref)
    build_python_language(rebuild=True)
    return py_language()
