from pathlib import Path
from threading import Semaphore
from typing import Optional

from tree_sitter import Language

_PACKAGE = Path(__file__).parent

_BUILD_INPUT = _PACKAGE / "src"
_BUILD_OUTPUT = _PACKAGE / "python-language.so"

_language_cache: Optional[Language] = None


def py_language(rebuild: bool = False) -> Language:
    global _language_cache
    if rebuild or not _language_cache:
        _language_cache = Language(build_python_language(rebuild=True), "python")
    assert _language_cache, "this should exist"
    return _language_cache


def build_python_language(
    rebuild: bool = False, _lock: Semaphore = Semaphore()
) -> Path:
    """compile the python language into a useable .so file"""
    assert _BUILD_INPUT.exists(), "the language files must be downloaded"

    if rebuild and _BUILD_OUTPUT.exists():
        _BUILD_OUTPUT.unlink()

    if _lock.acquire() and not _BUILD_OUTPUT.exists():
        build_successful = Language.build_library(str(_BUILD_OUTPUT), [str(_PACKAGE)])
        assert build_successful, "python tree-parser language failed to build"

    return _BUILD_OUTPUT
