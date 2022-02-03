from setuptools import find_packages, setup

setup(
    name='tree-sitter-python-language',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['tree_sitter'],
    setup_requires=['tree_sitter'],
)
