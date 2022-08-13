from setuptools import setup
from Cython.Build import cythonize

setup(
    name="raycaster",
    install_requires= ["pygame", "numpy"],
    url="https://github.com/SpieleentwicklungBodensee/raycaster",
    license="MIT",
    ext_modules = cythonize('fastfloor.pyx', language_level = 3)
)

# python setup.py build_ext --inplace
