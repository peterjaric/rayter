# encoding: utf-8

from setuptools import setup, find_packages
import sys, os

version = '2.1.0'

setup(
    name='rayter',
    version=version,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'rayter = rayter.main:main',
        ]
    },
)
