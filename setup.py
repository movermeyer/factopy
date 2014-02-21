# -*- coding: utf-8 -*-
try:
	from setuptools import setup
	from setuptools import find_packages
except ImportError:
	from distutils.core import setup

from pip.req import parse_requirements
reqs = [str(ir.req) for ir in parse_requirements('requirements.txt')]

setup(
	name='factopy',
	version='0.0.1',
	author=u'Eloy Adonis Colell',
	author_email='eloy.colell@gmail.com',
	packages=find_packages(),
	url='https://github.com/ecolell/factopy',
	license='GNU AGPL v3, see LICENCE.txt',
	description='This is a framework that provides certain abstract classes for distributed processing on a cluster.',
	long_description=open('README.md').read(),
	zip_safe=False,
	include_package_data=True,
	install_requires = reqs,
)