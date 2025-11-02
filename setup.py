
from setuptools import setup
import versioneer


# Read in long description
with open('README.rst', 'r') as buf:
    long_description = buf.read()

# Read in requirements.txt
with open('requirements.txt', 'r') as buf:
    requirements = buf.read().splitlines()


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
    ],
    install_requires=requirements,
    include_package_data=True,
    zip_safe=True,
)
