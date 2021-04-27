import io
from setuptools import setup, find_packages
import pathlib

with io.open("./requirements.txt") as f:
    requires = f.read().split('\n')

with io.open("./README.md") as f:
    readme = f.read()

setup(
    name='VMIntelligence',
    version='1.0.1',
    description='Remontees des cout des VM',
    packages=find_packages(exclude=('tests',)),
    long_description=readme,
    entry_points={'console_scripts': ['vmintelligence=content.main:main']},
    author='Camille SAURY, Daniel ADAM',
    install_requires=requires,
)
