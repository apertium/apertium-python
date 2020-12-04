#!/usr/bin/env python3

from os import path
import platform
import re
from typing import List

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def install_binaries() -> None:
    import apertium

    apertium.installer.nightly = True
    apertium.installer.install_apertium()
    apertium.installer.install_module('eng')
    apertium.installer.install_module('eng-spa')

    def kaz_tat_install():
        apertium.installer.nightly = False
        ubuntu = apertium.installer.Debian()
        if platform.system() == 'Linux':
            ubuntu._install_package_source()
        apertium.installer.install_module('kaz-tat')
        apertium.installer.nightly = True
        if platform.system() == 'Linux':
            ubuntu._install_package_source()
    kaz_tat_install()

    apertium.installer.install_wrapper('python3-apertium-core')
    apertium.installer.install_wrapper('python3-apertium-lex-tools')
    apertium.installer.install_wrapper('python3-cg3')
    apertium.installer.install_wrapper('python3-lttoolbox')
    apertium.installer.install_apertium_linux()


class CustomInstallCommand(install):
    def run(self) -> None:
        install.run(self)
        install_binaries()


class CustomDevelopCommand(develop):
    def run(self) -> None:
        develop.run(self)
        install_binaries()


def find_details(find_value: str, file_paths: List[str]) -> str:
    pwd = path.abspath(path.dirname(__file__))
    with open(path.join(pwd, *file_paths), 'r') as input_file:
        match = re.search(r"^__{}__ = ['\"]([^'\"]*)['\"]".format(find_value), input_file.read(), re.M)
    if match:
        return match.group(1)
    raise RuntimeError('Unable to find {} string.'.format(find_value))


setup(
    name='apertium',
    author=find_details('author', ['apertium', '__init__.py']),
    author_email='sushain@skc.name',
    license=find_details('license', ['apertium', '__init__.py']),
    version=find_details('version', ['apertium', '__init__.py']),
    keywords='apertium machine translation linguistics',
    description='Apertium core modules available in Python',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
    ],
    long_description=open(path.join(path.abspath(path.dirname(__file__)), 'README.md')).read(),
    long_description_content_type='text/markdown; charset=UTF-8',
    platforms=['Debian', 'Windows'],
    url='https://github.com/apertium/apertium-python',
    python_requires='>=3.5',
    setup_requires=[
        'apertium-streamparser==5.0.2',
    ],
    install_requires=[
        'apertium-streamparser==5.0.2',
    ],
    test_suite='tests',
    package_data={'apertium': ['py.typed']},
    packages=find_packages(exclude=['tests']),
    cmdclass={
        'develop': CustomDevelopCommand,
        'install': CustomInstallCommand,
    },
)
