"""Copyright since 2020, EPAM Systems

   This file is part of OSCI.

   OSCI is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   OSCI is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with OSCI.  If not, see <http://www.gnu.org/licenses/>."""

from setuptools import find_packages, setup
from osci import __version__


def readme():
    with open('README.md') as f:
        return f.read()


def requires():
    with open('osci/requirements.txt') as f:
        return f.read().splitlines()


setup(
    name='osci',
    packages=find_packages(exclude=['test', 'test.*', '__app__*']),
    setup_requires=['wheel'],
    package_dir={'osci': 'osci'},
    package_data={'osci': ['config/files/*.yml']},
    install_requires=requires(),
    version=__version__,
    description='OSCI, the Open Source Contributor Index',
    long_description=readme(),
    author='Vladislav Isayko, Aleksei Gavrilov, Ruslan Salikhov, Karim Safiullin',
    author_email='Vladislav_Isaiko@epam.com, Aleksei_Gavrilov1@epam.com, Ruslan_Salikhov@epam.com, Karim_Safiullin@epam.com',
    python_requires='>=3',
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.7',
        'Environment :: Console',
    ],
)
