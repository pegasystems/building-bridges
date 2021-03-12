from setuptools import setup, find_packages

setup(
    name='building-bridges',
    version='1.0.0',
    description='Building bridges',
    author='Meeples',

    packages=find_packages(),

    install_requires=['flask-restplus==0.13.0'],
)
