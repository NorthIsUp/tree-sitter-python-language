PACKAGE_VERSION := 0.13.1
GRAMMAR_VERSION := 0.19.0

TREE_SITTER_PYTHON_SRC := tree-sitter-python-$(GRAMMAR_VERSION)
TREE_SITTER_PYTHON_TGZ := https://github.com/tree-sitter/tree-sitter-python/archive/refs/tags/v$(GRAMMAR_VERSION).tar.gz

ifndef VIRTUAL_ENV
$(error VIRTUAL_ENV is not set, activate it plz)
endif
ifndef TWINE_USERNAME
$(error TWINE_USERNAME is not set)
endif
ifndef TWINE_PASSWORD
$(error TWINE_PASSWORD is not set)
endif


all: build

build/$(TREE_SITTER_PYTHON_SRC):
	@echo "--> creating $@"
	mkdir -p build
	curl -L -o build/$(TREE_SITTER_PYTHON_SRC).tar.gz $(TREE_SITTER_PYTHON_TGZ)
	tar -zxf build/$(TREE_SITTER_PYTHON_SRC).tar.gz --directory build

tree_sitter_python_language/_versions.py:
	@echo "--> creating $@"
	@echo > $@ '\
	# This file is autogenerated by make\n\
	# values can be changed in the Makefile\n\
	\n\
	# Version of this python package, used in setup.py\n\
	__version__ = "$(PACKAGE_VERSION)"\n\
	\n\
	# Version of the grammar pulled down during packaging\n\
	#   $(TREE_SITTER_PYTHON_TGZ)\n\
	__grammar_version__ = "$(GRAMMAR_VERSION)"'

pyproject.toml:
	@echo "--> creating $@"
	@echo > $@ '\
	[tool.poetry]\n\
	name="tree-sitter-python-language"\n\
	version="$(PACKAGE_VERSION)"\n\
	description="hi"\n\
	authors=["adam"]\n\
	include=[\n\
		"tree_sitter_python_language/src/**/*",\n\
	]\n\
	build = "build.py"\n\
	\n\
	[tool.poetry.dependencies]\n\
	python = "^3.7"\n\
	tree_sitter = "^0.20.0"\n\
	\n\
	[tool.poetry.dev-dependencies]\n\
	black = ""\n\
	mypy = ""\n\
	isort = ""\n\
	\n\
	[build-system]\n\
	requires = ["poetry_core>=1.0.0"]\n\
	build-backend = "poetry.core.masonry.api"'

deps: clean
# deps: pyproject.toml
deps: tree_sitter_python_language/_versions.py
deps: build/$(TREE_SITTER_PYTHON_SRC)
deps:
	cp -r \
		build/$(TREE_SITTER_PYTHON_SRC)/src \
		tree_sitter_python_language/src

build: clean deps
	pip install poetry
	python setup.py sdist

install: build
	python setup.py install

publish: clean build
	pip install twine && twine upload dist/*

clean:
	yes | pip uninstall tree_sitter_python_language
	rm -rf \
		build \
		dist \
		*egg-info \
		**/*.so \
		**/__pycache__ \
		tree_sitter_python_language/src \
		tree_sitter_python_language/_versions.py \
		pyproject.toml

format:
	pip install black
	black tree_sitter_python_language

build-debug: build
	cd dist && tar -zxf *.tar.gz
	@echo '-------------- build ---------------'
	tree build
	@echo '-------------- dist ---------------'
	tree dist
	python dist/tree-sitter-python-language-*/tree_sitter_python_language
