# -*- coding: utf-8 -*-
try:
	from setuptools import setup
	from setuptools import find_packages
except ImportError:
	from distutils.core import setup

setup(
	name='factopy',
	version='0.0.0',
	author=u'Eloy Adonis Colell',
	author_email='eloy.colell@gmail.com',
	packages=find_packages(),
	url='https://github.com/ecolell/factopy',
	license='GNU AGPL v3, see LICENCE.txt',
	description='This is a framework that provides certain abstract classes for distributed processing on a cluster.',
	long_description=open('README.md').read(),
	zip_safe=False,
	include_package_data=True,
	install_requires = [
		'Django == 1.5',
		'numpy == 1.8.0',
		'pytz == 2012j',
		'django-polymorphic == 0.5.3',
		'defusedxml == 0.4.1',
		'lxml == 2.3.6',
		'django-tastypie == 0.11.0'
		]
)