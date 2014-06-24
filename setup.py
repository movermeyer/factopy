# -*- coding: utf-8 -*-
try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    from distutils.core import setup

from pip.req import parse_requirements
reqs = [str(ir.req) for ir in parse_requirements('requirements.txt')]

# Try to transform the README from Markdown to reStructuredText.
try:
    import pandoc
    pandoc.core.PANDOC_PATH = 'pandoc'
    doc = pandoc.Document()
    doc.markdown = open('README.md').read()
    description = doc.rst
except ImportError:
    description = open('README.md').read()

setup(
    name='factopy',
    version='0.0.4',
    author=u'Eloy Adonis Colell',
    author_email='eloy.colell@gmail.com',
    packages=find_packages(),
    url='https://github.com/ecolell/factopy',
    license='GNU AGPL v3, see LICENCE.txt',
    description='A python framework that provides abstract classes for a high \
        performance computing cluster based in a pipe and filter architecture',
    long_description=description,
    zip_safe=False,
    include_package_data=True,
    install_requires=reqs,
)
