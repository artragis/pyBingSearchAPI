from distutils.core import setup
from setuptools import find_packages


setup(
    name='pyBingSearchAPI',
    version='1',
	install_requires=['requests'],
    url='https://github.com/artragis/pyBingSearchAPI',
    license='GPLv2',
    author='',
    author_email='',
    description='pyBingSearchAPI is a connector for Bing Search API for version 2.0 and later',
    long_description=open('README.md').read()
)
