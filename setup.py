# -*- coding: utf-8 -*-
# @Time    : 2020/10/30 8:07 下午
# @Author  : Henson
# @Email   : henson_wu@foxmail.com
# @File    : setup.py
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

install_packages = []
setup(
    name='flute',
    version='1.0',
    description='flute',
    long_description=readme,
    author='henson',
    author_email='henson_wu@foxmail.com',
    url='',
    packages=find_packages(exclude=('tests', 'docs', 'templates')),
    package_data={
        "flute": ["*.jar"]
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [

        ],
    },
)
