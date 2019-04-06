from setuptools import setup
from setuptools.command.install import install
from atexit import register
from os import path
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
    packages=['apertium', 'apertium.analysis',
              'apertium.generation', 'apertium.translation'],
    url='https://github.com/apertium/apertium-python',
    license='GNU General Public License v3.0 ',
    # author='',
    # author_email='',
    # description='',
    long_description=open(path.join(path.abspath(path.dirname(__file__)), 'README.md')).read(),
    python_requires='>=3.4',
    install_requires=[
        'apertium-streamparser==5.0.2',
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
)
