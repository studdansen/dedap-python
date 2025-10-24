'''
Package setup module.
'''

from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
	name='dedap',
	version='2025.10',
	description="Topological sorting and transitive reduction algorithms",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/studdansen/dedap",
	author="Dan Lynn",
	author_email="dan.lynn.ct@gmail.com",
	package_dir={"": "dedap"},
	packages=find_packages(where="dedap"),
	python_requires=">=3.7, <4"
)
