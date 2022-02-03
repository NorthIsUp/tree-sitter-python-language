ifndef VIRTUAL_ENV
$(error VIRTUAL_ENV is not set)
endif
ifndef TWINE_USERNAME
$(error TWINE_USERNAME is not set)
endif
ifndef TWINE_PASSWORD
$(error TWINE_PASSWORD is not set)
endif

build: clean
	python setup.py sdist

install: build
	python setup.py install

publish: build
	pip install twine && twine upload dist/*

clean:
	yes | pip uninstall tree_sitter_python_language
	rm -rf \
		build \
		dist \
		*egg-info \
		**/*.so \
		**/__pycache__

format:
	pip install black
	black tree_sitter_python_language
