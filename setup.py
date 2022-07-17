from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize('fastfloor.pyx', language_level = 3))

# python setup.py build_ext --inplace
