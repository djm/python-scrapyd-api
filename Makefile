.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "test-release - using TestPyPI"
	@echo "dist - package"

clean: clean-build clean-pyc
	rm -fr htmlcov/

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

test:
	python setup.py test

test-all:
	tox

coverage:
	py.test --cov-report html  --cov scrapyd_api tests/
	open htmlcov/index.html

docs:
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/build/html/index.html

release: clean
	python3 setup.py sdist bdist_wheel
	echo "You will be asked for auth TWICE, one for tar, one for wheel - until MD bug is resolved"
	# Tar must go first due to markdown render related bug with wheel
	# When wheel==0.31 is released, this can change to just one line with dist/*
	twine upload  --repository-url https://upload.pypi.org/legacy/ dist/*.tar.gz
	twine upload  --repository-url https://upload.pypi.org/legacy/ dist/*.whl

test-release: clean
	python3 setup.py sdist bdist_wheel
	echo "You will be asked for auth TWICE, one for tar, one for wheel - until MD bug is resolved"
	# Tar must go first due to markdown render related bug with wheel
	# When wheel==0.31 is released, this can change to just one line with dist/*
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*.tar.gz
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*.whl

dist: clean
	python3 setup.py sdist bdist_wheel
	ls -l dist
