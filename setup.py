# -*- coding: utf-8 -*-
import io
import versioneer

from setuptools import find_packages, setup


with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='djangoprj',
    version=versioneer.get_version(),
    url='https://sergelab.ru',
    cmdclass=versioneer.get_cmdclass(),
    author='Sergey Syrov',
    author_email='sergelab@gmail.com',
    description='Django App',
    long_description=readme,
    package_dir={'': 'src'},
    platforms='any',
    packages=find_packages(where='src'),
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5'
        'Programming Language :: Python :: 3.6'
        'Programming Language :: Python :: 3.7'
    ]
)
