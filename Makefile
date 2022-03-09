ifndef VIRTUAL_ENV
$(error VIRTUAL_ENV is not set)
endif
ifndef TWINE_USERNAME
$(error TWINE_USERNAME is not set)
endif
ifndef TWINE_PASSWORD
$(error TWINE_PASSWORD is not set)
endif

TREE_SITTER_PYTHON_VERSION := 0.19.0
TREE_SITTER_PYTHON_SRC := tree-sitter-python-$(TREE_SITTER_PYTHON_VERSION)

build/$(TREE_SITTER_PYTHON_SRC):
	mkdir -p build
	curl -L \
		-o build/$(TREE_SITTER_PYTHON_SRC).tar.gz \
		https://github.com/tree-sitter/tree-sitter-python/archive/refs/tags/v$(TREE_SITTER_PYTHON_VERSION).tar.gz
	tar -zxf build/$(TREE_SITTER_PYTHON_SRC).tar.gz --directory build

deps: clean build/$(TREE_SITTER_PYTHON_SRC)
	cp -r \
		build/$(TREE_SITTER_PYTHON_SRC)/src \
		tree_sitter_python_language/src

build: clean deps
	pip install poetry
	python setup.py sdist

install: build
	python setup.py install

publish: build
	pip install twine && twine upload dist/*

clean:
	yes | pip uninstall tree_sitter_python_language
	rm -rfv \
		build \
		dist \
		*egg-info \
		**/*.so \
		**/__pycache__ \
		tree_sitter_python_language/src \

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
