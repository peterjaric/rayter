# encoding: utf-8

from setuptools import setup, find_packages
import sys, os

version = '1.0.0'

setup(
    name='rayter',
    version=version,
    description="Game rating command line tool",
    long_description="""Game rating command line tool""",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Games/Entertainment",
    ],
    keywords='',
    author='Peter Jaric, Jonatan Heyman',
    author_email='peter@jaric.org, jonatan@heyman.info',
    url='https://github.com/peterjaric/rayter',
    license='MIT',
    platform='Any',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'rayter = rayter.main:main',
        ]
    },
)
