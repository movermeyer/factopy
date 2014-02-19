# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
	name='factopy',
	version='0.0.0',
	author=u'Eloy Adonis Colell',
	author_email='eloy.colell@gmail.com',
	packages=find_packages(),
	url='https://github.com/ecolell/factopy',
	license='GNU AGPL v3, see LICENCE.txt',
	description='This is a framework that provides certain abstract classes for distributed processing on a cluster.',
	long_description=open('README.txt').read(),
	zip_safe=False,
	include_package_data=True,
)