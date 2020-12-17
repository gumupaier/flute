# -*- coding: utf-8 -*-
# @Time    : 2020/10/30 8:07 下午
# @Author  : Henson
# @Email   : henson_wu@foxmail.com
# @File    : setup.py
from setuptools import setup, find_packages

# with open('README.md') as f:
#     readme = f.read()

readme = """
please see https://github.com/gumupaier/flute
"""

install_packages = []
setup(
    name='nebula_flute',
    version='1.0.5',
    description='nebula graph database toolkit python version',
    long_description=readme,
    author='henson',
    author_email='henson_wu@foxmail.com',
    url='https://github.com/gumupaier/flute',
    packages=find_packages(exclude=('tests', 'docs', 'templates')),
    package_data={
        "": ["*.jar", "flute/apps/amber/template/*"],
    },
    install_requires=[
        'aiomysql',
        'blessed',
        'cffi',
        'cryptography',
        'future',
        'gevent',
        'greenlet',
        'httplib2',
        'inquirer',
        'nebula-python',
        'pycparser',
        'PyMySQL',
        'python-editor',
        'PyYAML',
        'readchar',
        'six',
        'click',
        'wcwidth',
        'zope.event',
        'zope.interface',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'flute=flute.commands.command:main'
        ],
    },
)
