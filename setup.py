from setuptools import setup, find_packages
import os

version = {}
with open(os.path.join("ghostpath", "version.py")) as f:
    exec(f.read(), version)

setup(
    name="GhostPath",
    version="2.3.6",
    author="Atharv Yadav",
    description="GhostPath - Interactive Recon Shell for Ethical Hackers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/atharvbyadav/GhostPath",
    packages=find_packages(include=["ghostpath", "ghostpath.*"]),
    include_package_data=True,
    package_data={"ghostpath.data": ["*.txt"]},
    install_requires=[
        "requests>=2.31.0",
        "colorama>=0.4.6"
    ],
    entry_points={
        "console_scripts": [
            "GhostPath=ghostpath.main:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires=">=3.7",
)
