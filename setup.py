from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="recycle",
    version="1.1.0",
    description="A utility to help recycle commonly use files and templates.",
    url="http://williamg.me/recycle",
    author="William Ganucheau",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Utilities"
    ],
    keywords="productivity utility",
    packages=["recycle"],
    entry_points={
        "console_scripts": [
            "re=recycle:main",
        ],
    }
)
