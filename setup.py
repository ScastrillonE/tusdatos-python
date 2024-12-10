from setuptools import setup, find_packages

setup(
    name="tusdatos-python",
    version="1.0.0",
    description="TusDatos Python API Client",
    author="SCastrillonE",
    author_email="santiagocastrillon.ep@gmail.com",
    url="https://github.com/ScastrillonE/tusdatos-python",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)