from setuptools import setup, find_packages
import os

version = {}
with open(os.path.join("ghostpath", "version.py")) as f:
    exec(f.read(), version)

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="GhostPath",
    version=version["__version__"],
    author="Atharv Yadav",
    description="GhostPath - Interactive Recon Shell for Ethical Hackers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atharvbyadav/GhostPath",
    license="BSD-3-Clause",
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
    keywords=["osint", "recon", "security", "hacking", "penetration-testing", "cli"],
    project_urls={
        "Documentation": "https://github.com/atharvbyadav/GhostPath",
        "Source": "https://github.com/atharvbyadav/GhostPath",
        "Tracker": "https://github.com/atharvbyadav/GhostPath/issues",
    },
)
