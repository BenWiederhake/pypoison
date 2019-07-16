#!/usr/bin/env python3
# Copyright (c) 2019, Ben Wiederhake
# MIT license.  See the LICENSE file included in the package.

import os.path
from setuptools import setup

from os import path


this_directory = os.path.abspath(path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pypoison',
    version='0.0.1',
    packages=['pypoison'],
    install_requires=[],
    author='Ben Wiederhake',
    author_email='BenWiederhake.GitHub@gmx.de',
    description='Nothing says "DO NOT USE" like a poison value.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    platforms='Any',
    license='MIT',
    keywords='pypoison',
    url='https://github.com/BenWiederhake/pypoison',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
