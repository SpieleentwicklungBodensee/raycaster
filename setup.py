from setuptools import setup, Extension, find_packages

setup(
    name="raycaster",
    install_requires= ["pygame", "numpy"],
    url="https://github.com/SpieleentwicklungBodensee/raycaster",
    license="MIT",
    packages=["raycaster"],
    ext_modules = [
        Extension(
            "raycaster.fastfloor",
            sources=["raycaster/fastfloor.pyx"],
        ),
    ],
    package_data = {
        "raycaster": ["textures/*"]
    },
)
