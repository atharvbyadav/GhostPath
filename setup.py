from setuptools import setup, find_packages

setup(
    name="GhostPath",
    version="1.0.0",
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
