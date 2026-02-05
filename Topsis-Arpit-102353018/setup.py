from setuptools import setup, find_packages

setup(
    name="Topsis-Arpit-102353018",
    version="1.0.0",
    author="Arpit",
    author_email="agarwalarpit485@gmail.com",
    description="Implementation of TOPSIS method as a Python package",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy"
    ],
    entry_points={
        "console_scripts": [
            "topsis=topsis_arpit_102353018.topsis:main"
        ]
    },
    python_requires=">=3.7",
)
