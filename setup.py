from setuptools import find_packages, setup

setup(
    name="tree-sitter-python-language",
    version="0.0.5",
    packages=find_packages(),
    requires=["tree_sitter", "requests"],
)
