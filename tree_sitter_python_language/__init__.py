from pathlib import Path
from urllib import response

from tree_sitter import Language

_PACKAGE = Path(__file__).parent

BUILD_INPUT = _PACKAGE / 'vendor' / 'tree-sitter-python'
BUILD_OUTPUT = _PACKAGE / 'python-language.so'
TREE_SITTER_ZIP_URL = 'https://codeload.github.com/tree-sitter/tree-sitter-python/zip/refs/heads/master'

def build_python_language(rebuild: bool = False) -> Path:
    """compile the python language into a useable .so file"""
    assert BUILD_INPUT.exists(), 'the language files must be downloaded'

    if BUILD_OUTPUT.exists() and rebuild:
        BUILD_OUTPUT.unlink()
    
    if not BUILD_OUTPUT.exists():
        build_successful = Language.build_library(str(BUILD_OUTPUT), [str(BUILD_INPUT)])
        assert build_successful, 'python tree-parser language failed to build'

    return BUILD_OUTPUT

def py_language() -> Language:
    return Language(build_python_language(rebuild=False), 'python')

def download_and_extract_language_zip():
    import zipfile
    from io import BytesIO

    import requests

    response = requests.get(TREE_SITTER_ZIP_URL)

    # extracting the zip file contents but remove the top level dirname
    with zipfile.ZipFile(BytesIO(response.content)) as zip:
        for zip_info in zip.infolist():
            if zip_info.filename[-1] == '/':
                continue
            zip_info.filename = '/'.join(zip_info.filename.split('/')[1:])
            zip.extract(zip_info, BUILD_INPUT)
