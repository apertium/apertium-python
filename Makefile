SHELL := /bin/bash

dist:
	git clean -xfd
	./setup.py sdist

release: dist
	twine upload --sign dist/*

test-release: dist
	twine upload --sign --repository-url https://test.pypi.org/legacy/ dist/*
