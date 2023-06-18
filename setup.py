from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in tx_manager/__init__.py
from tx_manager import __version__ as version

setup(
	name="tx_manager",
	version=version,
	description="A simple app to reconcile your transactions",
	author="The Commit Company",
	author_email="nikhil.kothari@thecommit.company",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
