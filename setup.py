from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in food_beverages/__init__.py
from food_beverages import __version__ as version

setup(
	name="food_beverages",
	version=version,
	description="Food and Beverages Module",
	author="Surya",
	author_email="suryakannan@agnikul.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
