from pathlib import Path

from tree_sitter import Language

_PACKAGE = Path(__file__).parent
_PACKAGE_ROOT = _PACKAGE.parent

BUILD_INPUT = _PACKAGE_ROOT / 'vendor' / 'tree-sitter-python'
BUILD_OUTPUT = _PACKAGE / 'python-language.so'

def build_python_language(rebuild: bool = False) -> Path:
    """compile the python language into a useable .so file"""
    assert BUILD_INPUT.exists(), f'{BUILD_INPUT} is missing, it is required to build the language file'

    if BUILD_OUTPUT.exists() and rebuild:
        BUILD_OUTPUT.unlink()
    
    if not BUILD_OUTPUT.exists():
        build_successful = Language.build_library(str(BUILD_OUTPUT), [str(BUILD_INPUT)])
        assert build_successful, 'python tree-parser language failed to build'

    return BUILD_OUTPUT

def py_language() -> Language:
    return Language(build_python_language(rebuild=False), 'python')
