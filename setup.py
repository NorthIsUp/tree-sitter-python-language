# -*- coding: utf-8 -*-
import sys
from cmath import log
from distutils import log as logger
from distutils.command.build_ext import build_ext
from distutils.core import Extension, setup
from glob import glob
from pathlib import Path
from pprint import pformat
from typing import Any, Dict

package_name = "tree-sitter-python-language"
package_under = package_name.replace("-", "_")
package_library = "python-language.so"

# add tree_sitter_python_language to prevent __init__ from running
sys.path.append(str(Path(__file__).parent / package_under))

try:
    from _versions import __grammar_version__, __version__
except ModuleNotFoundError as e:
    raise ModuleNotFoundError("Run 'make build' before using setup.py") from e

packages = [package_under]

package_data = {
    "": ["*"],
    package_under: [package_library, "src/*", "src/tree_sitter/*"],
}

requirements = ["tree_sitter>=0.20.0,<0.21.0"]


tree_sitter_extension = Extension(
    "tree_sitter_builder",
    # sources=[str(_) for _ in (Path(package_under) / "src").glob("**")],
    sources=[],
    libraries=[package_library],
)


class tree_sitter_build_ext(build_ext, object):
    """
    Specialized builder for testlib library

    """

    def build_extension(self, ext: Extension):
        if ext is tree_sitter_extension:
            self.build_tree_sitter_extension(ext)
        else:
            super().build_extension(ext)

    def build_tree_sitter_extension(self, ext: Extension):
        logger.info("Building python-language.so")
        from tree_sitter_python_language import build_python_language

        build_python_language(
            rebuild=True, build_lib=Path(self.build_lib) / package_under
        )


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
    "setup_requires": requirements,
    "install_requires": requirements,
    "python_requires": ">=3.7,<4.0",
    "ext_modules": [tree_sitter_extension],
    "cmdclass": {"build_ext": tree_sitter_build_ext},
}

setup(**setup_kwargs)
