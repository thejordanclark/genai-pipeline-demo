from setuptools import setup, find_packages

setup(
    name="clinical-validation-system",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pytest>=7.4.3",
        "pandas>=2.1.3",
        "jsonschema>=4.20.0",
    ],
    python_requires=">=3.9",
    author="Clinical Validation Team",
    description="GxP-validated clinical trial data processing system",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Programming Language :: Python :: 3.9",
    ],
)
