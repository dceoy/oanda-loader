#!/usr/bin/env python

from setuptools import find_packages, setup

from oandacli import __version__

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='oanda-cli',
    version=__version__,
    description='Command Line Interface for Oanda API',
    packages=find_packages(),
    author='Daichi Narushima',
    author_email='dnarsil+github@gmail.com',
    url='https://github.com/dceoy/oanda-cli',
    include_package_data=True,
    install_requires=[
        'docopt', 'pandas', 'pyyaml', 'redis', 'ujson', 'v20'
    ],
    entry_points={
        'console_scripts': ['oanda-cli=oandacli.cli.main:main'],
    },
    classifiers=[
        'Development Status :: 3 - Beta',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment'
    ],
    python_requires='>=3.6',
    long_description=long_description
)
