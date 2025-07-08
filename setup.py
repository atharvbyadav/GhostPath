from setuptools import setup, find_packages
import os

version = {}
with open(os.path.join("ghostpath", "version.py")) as f:
    exec(f.read(), version)

setup(
    name="GhostPath",
    version="2.3.5",
    description="GhostPath - Interactive Recon Shell for Ethical Hackers",
    author="Atharv Yadav",
    packages=find_packages(),
    include_package_data=True,
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
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
