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
    description="GhostPath v3.0 - Modular Recon Intelligence Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atharvbyadav/GhostPath",
    license="BSD-3-Clause",
    packages=find_packages(include=["ghostpath", "ghostpath.*"]),
    include_package_data=True,
    package_data={
        "ghostpath": ["tui/themes/*.css"],
        "ghostpath.data": ["*.txt", "wordlists/*.txt"],
    },
    install_requires=[
        "aiohttp>=3.9.5",
        "beautifulsoup4>=4.12.3",
        "builtwith>=1.3.4",
        "httpx>=0.27.0",
        "playwright>=1.52.0",
        "PyYAML>=6.0.2",
        "requests>=2.31.0",
        "rich>=13.7.1",
        "textual>=0.61.1",
        "tldextract>=5.1.2",
    ],
    entry_points={
        "console_scripts": [
            "ghostpath=ghostpath.main:main",
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
    python_requires=">=3.11",
    keywords=["osint", "recon", "security", "hacking", "penetration-testing", "tui"],
    project_urls={
        "Documentation": "https://github.com/atharvbyadav/GhostPath",
        "Source": "https://github.com/atharvbyadav/GhostPath",
        "Tracker": "https://github.com/atharvbyadav/GhostPath/issues",
    },
)
