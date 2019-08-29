SHELL := /bin/bash

dist:
	./setup.py sdist

release:
	./setup.py sdist bdist_wheel
	twine upload --sign dist/*

test-release:
	./setup.py sdist bdist_wheel
	twine upload --sign --repository-url https://test.pypi.org/legacy/ dist/*
