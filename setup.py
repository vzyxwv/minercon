#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys

from setuptools import find_packages, setup


# Import the README and use it as the long-description.
with io.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'),
             encoding='utf-8') as f:
    long_description = '\n' + f.read()


setup(
    name='minercon',
    version='0.1.1',
    description='A Python2/3 RCON client for Minecraft',
    long_description=long_description,
    author='CraftySpaz',
    url='https://github.com/CraftySpaz/minercon',
    scripts=['minercon.py'],
    install_requires=[
        "MCRcon==0.0.0"
    ],
    dependency_links=[
        "git+https://github.com/CraftySpaz/MCRcon.git#egg=MCRcon-0.0.0"
    ],
    include_package_data=True,
    license='MIT'
)
