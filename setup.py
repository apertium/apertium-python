from setuptools import setup
from setuptools.command.install import install
from atexit import register
import installation


class PostInstallCommand(install):
    def __init__(self, *args, **kwargs):
        super(PostInstallCommand, self).__init__(*args, **kwargs)
        register(self._post_install)

    @staticmethod
    def _post_install():
        installation.main()


setup(
    name='apertium-python',
    # version='',
    packages=['tests', 'apertium', 'apertium.analysis',
              'apertium.generation', 'apertium.translation'],
    url='https://github.com/apertium/apertium-python',
    license='GNU General Public License v3.0 ',
    # author='',
    # author_email='',
    # description='',
    long_description=open('README.md').read(),
    install_requires=[
        'apertium-streamparser==5.0.2',
    ],
    setup_requires=[
        'urllib3>=1.24.1',
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
)
