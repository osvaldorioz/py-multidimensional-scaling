from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
    Pybind11Extension(
        "mds_module",
        ["mds2.cpp"],
        include_dirs=["/usr/include/eigen3"],  # Asegurar que se incluya Eigen
        extra_compile_args=["-O3"],  # Optimización
    )
]

setup(
    name="mds_module",
    version="1.0",
    ext_modules=ext_modules,
    zip_safe=False,
)
