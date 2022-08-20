#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join, dirname


setup(
    name='rest_test',
    version='0.1.1',
    # url='https://github.com/nikita0607/pargo',
    license='MIT',

    author="nikita0607",
    author_email="ecfed205@gmail.com",

    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),

    install_requires=[],

    entry_points = {
        "console_scripts": [
            "rest-test=rest_test:run"
        ]
    }
)
