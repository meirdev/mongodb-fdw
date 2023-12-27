from setuptools import setup

setup(
    name="mongodb-fdw",
    version="0.0.1",
    license="MIT",
    packages=["mongodb_fdw"],
    install_requires=["pymongo"],
)
