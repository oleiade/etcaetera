#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from distutils.core import Command

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='etcaetera',
    version='0.4.3',
    description='Manage multiple configuration sources in a single place',
    long_description=readme + '\n\n' + history,
    author='Oleiade',
    author_email='tcrevon@gmail.com',
    url='https://github.com/oleiade/etcaetera',
    packages=[
        'etcaetera',
        'etcaetera.adapter',
    ],
    package_dir={'etcaetera': 'etcaetera'},
    include_package_data=True,
    install_requires=[
        'PyYaml',
    ],
    license="MIT",
    zip_safe=False,
    keywords='etcaetera',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    cmdclass={'test': PyTest},
)
