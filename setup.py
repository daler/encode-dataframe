from setuptools import setup, find_packages
from os import path
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='encode-dataframe',
    version='0.1',
    description="Convert UCSC's ENCODE metadata into pandas DataFrames",
    long_description=long_description,
    author='Ryan Dale',
    author_email='dalerr@niddk.nih.gov',
    license='MIT',
    install_requires=['pandas'],
)
