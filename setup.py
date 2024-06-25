from pybind11.setup_helpers import Pybind11Extension, build_ext
from glob import glob
from setuptools import setup

ext_modules = [
    Pybind11Extension(
        "iot",
        sorted(glob("iot.cpp")),
    ),
]


setup(
    name="iot",
    version="1.0",
    author="Roger Huauya",
    description="Simple API for IoT devices monitoring.",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext}
)