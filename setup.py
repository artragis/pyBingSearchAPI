from distutils.core import setup
from setuptools import find_packages
import bing_search_api

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
setup(
    name='pyBingSearchAPI',
    version='1',
    packages=find_packages,
    url='https://github.com/artragis/pyBingSearchAPI',
    license='GPLv2',
    author='',
    author_email='',
    description='pyBingSearchAPI is a connector for Bing Search API for version 2.0 and later',
    install_requires=REQUIREMENTS,
    long_description=open('README.md').read()
)
