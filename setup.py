# -*- coding: utf-8 -*-

from os.path import join
from setuptools import setup, find_packages


version = '0.2'

install_requires = [
    'setuptools',
    'dolmen.collection >= 0.3',
    'zope.interface',
    'zope.schema',
    'zope.component',
    ]

tests_require = [
    ]

setup(
    name='dolmen.workflow',
    version=version,
    description="A workflow system based on transaction and states",
    long_description=(open("README.txt").read() + "\n" +
                      open(join("docs", "HISTORY.txt")).read()),
    keywords="Workflow Dolmen",
    author="Souheil Chelfouh",
    author_email="trollfot@gmail.com",
    url="http://gitweb.dolmen-project.org",
    license="ZPL",
    classifiers=[
        "Programming Language :: Python",
        ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    namespace_packages=['dolmen'],
    extras_require={'test': tests_require},
    install_requires=install_requires,
    )
