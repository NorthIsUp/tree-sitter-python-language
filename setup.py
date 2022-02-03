from setuptools import find_packages, setup

from tree_sitter_python_language import BUILD_OUTPUT

if not BUILD_OUTPUT.exists():
    import subprocess
    subprocess.check_output(["python3", "tree_sitter_python_language"])
    assert BUILD_OUTPUT.exists(), f'build failed, {BUILD_OUTPUT} does not exist'

setup(
    packages=find_packages(),
    package_data={'': [str(BUILD_OUTPUT)]},
    include_package_data=True,
    install_requires=['tree_sitter'],
    setup_requires=['tree_sitter'],
)
