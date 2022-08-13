from setuptools import setup, Extension
import sys

ext = '.c'
if '--cythonize' in sys.argv: 
    ext = '.pyx' 
    sys.argv.remove('--cythonize') # To avoid error option not recognized

cy_extension = Extension(name='fastfloor', sources=['fastfloor' + ext])
cy_extension.cython_directives = {'language_level': '3'}

setup(
    ext_modules=[cy_extension],
)

# Normal installation (without cython):
# python setup.py build_ext --inplace

# If you want to change fastfloor.pyx (need cython):
# python setup.py build_ext --inplace --cythonize 