# -*- coding: utf-8 -*-
from typing import Any, Dict

from setuptools import setup

from tree_sitter_python_language import __grammar_version__, __version__

packages = ["tree_sitter_python_language"]

package_data = {
    "": ["*"],
    "tree_sitter_python_language": ["src/*", "src/tree_sitter/*"],
}

install_requires = ["tree_sitter>=0.20.0,<0.21.0"]

setup_kwargs: Dict[str, Any] = {
    "name": "tree-sitter-python-language",
    "version": __version__,
    "description": f"A pip-installable version of tree-sitter-python-language-v{__grammar_version__}",
    "long_description": None,
    "author": "adam",
    "author_email": None,
    "maintainer": None,
    "maintainer_email": None,
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.7,<4.0",
}

setup(**setup_kwargs)
