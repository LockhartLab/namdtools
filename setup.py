"""
setup.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

import numpy as np
import os.path
from setuptools import Extension, setup
import versioneer

from Cython.Build import cythonize

# Read in long description
with open('README.rst', 'r') as stream:
    long_description = stream.read()

# Read in requirements.txt
with open('requirements.txt', 'r') as stream:
    requirements = stream.read().splitlines()


# Cython code
ext_modules = [
    Extension('namdtools.io._read_utils', [os.path.join('namdtools', 'io', '_read_utils.pyx')],
              include_dirs=[np.get_include()]),
]


# Setup
setup(
    name='namdtools',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='C. Lockhart',
    author_email='clockha2@gmu.edu',
    description='A Python interface to NAMD',
    long_description=long_description,
    # long_description_content_type='text/markdown',
    url="https://www.lockhartlab.org",
    packages=[
        'namdtools',
        'namdtools.analysis',
        'namdtools.core',
        'namdtools.io'
    ],
    install_requires=requirements,
    include_package_data=True,
    zip_safe=True,
    ext_modules=cythonize(ext_modules),
)
