from pathlib import Path
from threading import Semaphore
from typing import Optional, Union

from tree_sitter import Language

_PACKAGE = Path(__file__).parent

_BUILD_INPUT = _PACKAGE / "src"
_BUILD_TARGET = "python-language.so"

_language_cache: Optional[Language] = None


def py_language(rebuild: bool = False) -> Language:
    global _language_cache
    if rebuild or not _language_cache:
        _language_cache = Language(
            build_python_language(rebuild=rebuild, build_lib=_PACKAGE),
            "python",
        )
    assert _language_cache, "this should exist"
    return _language_cache


def build_python_language(
    rebuild: bool = False,
    build_lib: Union[str, Path] = _PACKAGE,
    _lock: Semaphore = Semaphore(),
) -> Path:
    """compile the python language into a useable .so file"""
    assert _BUILD_INPUT.exists(), "the language files must be downloaded"

    target = Path(build_lib) / _BUILD_TARGET

    if rebuild and target.exists():
        target.unlink()

    with _lock:
        if not target.exists():
            build_successful = Language.build_library(str(target), [str(_PACKAGE)])
            assert build_successful, "python tree-parser language failed to build"

    return target
