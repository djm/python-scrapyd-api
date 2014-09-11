#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

tests_require = ['mock', 'responses']
docs_require = ['sphinx']


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    print("You probably want to also git tag the version now.")
    sys.exit()


setup(
    name='python-scrapyd-api',
    version='0.1.0',
    description='A Python wrapper for working with the Scrapyd API',
    keywords='python-scrapyd-api scrapyd scrapy api wrapper',
    long_description=readme + '\n\n' + history,
    author='Darian Moody',
    author_email='mail@djm.org.uk',
    url='https://github.com/djm/python-scrapyd-api',
    packages=[
        'scrapyd_api',
    ],
    package_dir={
        'scrapyd_api': 'scrapyd_api'
    },
    include_package_data=True,
    install_requires=[
        'requests'
    ],
    license="BSD",
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
    ],
    cmdclass={
        'test': PyTest
    },
    extras_require={
        'tests': tests_require,
        'docs': docs_require
    },
    tests_require=tests_require
)
