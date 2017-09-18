from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# get the long description from the README file.
with open(path.join(here, 'README.rst'), encoding='utf-8') as stream:
    long_description = stream.read()

install_requires = [
    'click',
    'pandas>=0.19.1'
]

setup(
    name = "soldi",
    version = "0.0",

    description = "A CLI application of 'Kakeibo' which is Japanese household finance ledger.",
    long_description = long_description,

    author = "utahkaA",
    author_email = "utahka.akiba@gmail.com",
    liense = "MIT",

    install_requires = install_requires,

    entry_points={
        "console_scripts": [
            'soldi = soldi.__main__:main',
        ],
    }
)
