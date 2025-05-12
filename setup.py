#!/usr/bin/env python3
# setup.py

import io
import os
from setuptools import setup, find_packages

# Read the long description from README.md
here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="resonance_sandbox",
    version="0.2.0",
    description="An advanced framework for Semantic–Physical Resonance exploration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Phillip Holland",
    author_email="pholland@example.com",
    url="https://github.com/your-org/resonance_sandbox",
    license="MIT",
    classifiers=[
        # How mature is this project? Common values: 
        #   3 - Alpha, 4 - Beta, 5 - Production/Stable
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    keywords="semantic resonance geometry manifold AI research toolkit",
    packages=find_packages(exclude=["tests", "assets", "config"]),
    include_package_data=True,  # include files specified in MANIFEST.in
    install_requires=[
        "numpy>=1.20",
        "PyYAML>=5.4",
        "networkx>=2.6",
        "matplotlib>=3.4",
        "tqdm>=4.0"
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "flake8",
            "black",
            "mypy"
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme"
        ]
    },
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "resonance-sandbox = resonance_sandbox.sandbox:main"
        ]
    },
    project_urls={
        "Bug Tracker": "https://github.com/your-org/resonance_sandbox/issues",
        "Documentation": "https://your-org.github.io/resonance_sandbox/",
        "Source Code": "https://github.com/your-org/resonance_sandbox",
    },
    zip_safe=False,
)
