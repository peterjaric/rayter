# encoding: utf-8

from setuptools import setup, find_packages
import sys, os

version = '0.1.6'
 
setup(
    name='rayter',
    version=version,
    description="Game rating command line tool",
    long_description="""Game rating command line tool""",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
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
    #test_suite='rayter.test.runtests',
)
