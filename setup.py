# -*- coding: utf-8 -*-
import sys
from distutils.core import setup
from typing import Any, Dict

package_name = "tree-sitter-python-language"
package_under = package_name.replace("-", "_")

# add tree_sitter_python_language to prevent __init__ from running
sys.path.append(package_under)

from _versions import __grammar_version__, __version__

packages = [package_under]

package_data = {
    "": ["*"],
    package_under: ["src/*", "src/tree_sitter/*"],
}

requirements = ["tree_sitter>=0.20.0,<0.21.0"]

setup_kwargs: Dict[str, Any] = {
    "name": package_name,
    "version": __version__,
    "description": f"A pip-installable version of {package_name}-v{__grammar_version__}",
    "long_description": None,
    "author": "adam",
    "author_email": None,
    "maintainer": None,
    "maintainer_email": None,
    "url": "https://github.com/NorthIsUp/tree-sitter-python-language",
    "packages": packages,
    "package_data": package_data,
    "install_requires": requirements,
    "python_requires": ">=3.7,<4.0",
}

setup(**setup_kwargs)
