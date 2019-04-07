from atexit import register
from os import path
from setuptools import setup, find_packages
from setuptools.command.install import install

import installer


class PostInstallCommand(install):
    def __init__(self, *args, **kwargs):
        super(PostInstallCommand, self).__init__(*args, **kwargs)
        register(self._post_install)

    @staticmethod
    def _post_install():
        installer.install_apertium_windows()


setup(
    name='apertium-python',
    # version='',
    license='GNU General Public License v3.0 ',
    # description='',
    long_description=open(path.join(path.abspath(path.dirname(__file__)), 'README.md')).read(),
    long_description_content_type='text/markdown; charset=UTF-8',
    # keywords='',
    # author='',
    # author_email='',
    url='https://github.com/apertium/apertium-python',
    python_requires='>=3.4',
    install_requires=[
        'apertium-streamparser==5.0.2',
    ],
    packages=find_packages(exclude=['tests']),
    cmdclass={
        'install': PostInstallCommand,
    },
)
