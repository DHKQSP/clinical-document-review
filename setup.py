"""Setup script for Clinical Document Review Tool"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="clinical-document-review",
    version="1.0.0",
    description="Local clinical document review tool for Protocol, IB, and SAP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Clinical Research Team",
    python_requires=">=3.8",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pdfplumber>=0.10.3",
        "python-docx>=1.1.0",
        "openpyxl>=3.1.2",
        "PyPDF2>=3.0.1",
        "requests>=2.31.0",
        "click>=8.1.7",
        "jinja2>=3.1.3",
        "pyyaml>=6.0.1",
        "tqdm>=4.66.1",
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "clinical-review=cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="clinical-research protocol IB SAP document-review regulatory",
)
