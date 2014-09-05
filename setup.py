#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='djangorest-alchemy',
    version='0.1.1',
    description='Django REST Framework and SQLAlchemy integration',
    long_description=readme + '\n\n' + history,
    author='Ashish Gore',
    author_email='ashish.gore@dealertrack.com',
    url='https://github.com/Dealertrack/djangorest-alchemy',
    packages=[
        'djangorest_alchemy',
    ],
    package_dir={'djangorest_alchemy':
                 'djangorest_alchemy'},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='djangorest-alchemy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='djangorest_alchemy.tests',
)
