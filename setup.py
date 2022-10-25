import sys
from typing import List

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = [
    "rich",
    "click",
    "colorlog",
    "requests",
]


python_version = sys.version_info

test_requirements: List[str] = []

setup(
    name="eds",
    version="0.2.0",
    description="Energy Data Service",
    long_description=readme,
    author="Glen Harmon",
    author_email="glencharmon@gmail.com",
    url="",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    package_dir={"eds": "eds"},
    entry_points={"console_scripts": ["eds=eds.cli:commands"]},
    include_package_data=True,
    install_requires=requirements,
    license="Proprietary",
    zip_safe=False,
    keywords="eds",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "License :: Other/Proprietary License",
    ],
    test_suite="tests",
    tests_require=test_requirements,
)
