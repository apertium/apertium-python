from atexit import register
from os import path
from setuptools import find_packages, setup  # noqa: I202
from setuptools.command.install import install


class PostInstallCommand(install):
    def __init__(self, *args, **kwargs):
        super(PostInstallCommand, self).__init__(*args, **kwargs)
        register(self._post_install)

    @staticmethod
    def _post_install():
        import apertium
        apertium.installer.install_language_pack(['apertium-eng', 'apertium-en-es'], install_base=True)


setup(
    name='apertium-python',
    # TODO: Add version description, keywords, author, author_email
    license='GNU General Public License v3.0 ',
    long_description=open(path.join(path.abspath(path.dirname(__file__)), 'README.md')).read(),
    long_description_content_type='text/markdown; charset=UTF-8',
    url='https://github.com/apertium/apertium-python',
    python_requires='>=3.4',
    install_requires=[
        'apertium-streamparser==5.0.2',
        'distro',
    ],
    test_suite='tests',
    packages=find_packages(exclude=['tests']),
    cmdclass={
        'install': PostInstallCommand,
    },
)
