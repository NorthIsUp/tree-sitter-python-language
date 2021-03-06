PACKAGE_VERSION := 0.14.0
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

deps/$(TREE_SITTER_PYTHON_SRC).tar.gz:
	mkdir -p deps
	curl -L -o deps/$(TREE_SITTER_PYTHON_SRC).tar.gz $(TREE_SITTER_PYTHON_TGZ)

build/$(TREE_SITTER_PYTHON_SRC): deps/$(TREE_SITTER_PYTHON_SRC).tar.gz
	@echo "--> creating $@"
	mkdir -p build
	tar -zxf deps/$(TREE_SITTER_PYTHON_SRC).tar.gz --directory build

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

deps: clean
deps: tree_sitter_python_language/_versions.py
deps: build/$(TREE_SITTER_PYTHON_SRC)
deps:
	cp -r \
		build/$(TREE_SITTER_PYTHON_SRC)/src \
		tree_sitter_python_language/src

build: clean deps
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
		tree_sitter_python_language/_versions.py

format:
	pip install black
	black tree_sitter_python_language

build-debug: build
	cd dist && tar -zxf *.tar.gz
	@echo '-------------- build ---------------'
	tree build
	@echo '-------------- dist ---------------'
	tree dist

test: build-debug
	virtualenv-this --python python3.10 --clear scratch
	source ~/.virtualenvs/scratch/bin/activate && pip -vv install ~/src/tree-sitter-python-language/dist/tree-sitter-python-language-0.13.2.tar.gz
	tree ~/.virtualenvs/scratch/lib/python3.10/site-packages/tree_sitter_python_language/
