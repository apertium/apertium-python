from distutils.dir_util import copy_tree
import logging
import os
import platform
import shutil
import subprocess
import tempfile
from typing import Dict, Optional, Union
from urllib.request import urlretrieve
from zipfile import ZipFile

import apertium


nightly: bool = True


class Windows:
    """Download ApertiumWin64 and Move to %localappdata%"""
    base_link = 'http://apertium.projectjj.com/{}'

    def __init__(self) -> None:
        self._install_path: str = str(os.getenv('LOCALAPPDATA'))
        self._apertium_path: str = str(os.path.join(self._install_path, 'apertium-all-dev'))
        self._download_path = tempfile.mkdtemp()
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)

    def _download_zip(self, download_files: Dict[str, str], extract_path: Optional[str]) -> None:
        for zip_name, zip_link in download_files.items():
            zip_download_path = os.path.join(self._download_path, zip_name)
            urlretrieve(Windows.base_link.format(zip_link), filename=zip_download_path)
            self._logger.info('%s -> %s download completed', Windows.base_link.format(zip_link), zip_name)

            # Extract the zip
            with ZipFile(zip_download_path) as zip_file:
                zip_file.extractall(path=extract_path)
            self._logger.info('%s Extraction completed', zip_name)
            os.remove(zip_download_path)
            self._logger.info('%s removed', zip_name)

    def _download_package(self, package: str) -> None:
        """Installs Packages to %localappdata%/Apertium"""

        install_sh = 'nightly' if nightly else 'release'
        zip_path = f'win32/{install_sh}/data.php?zip='
        package_zip = {package: zip_path + package}
        self._download_zip(package_zip, self._download_path)

        # move the extracted files to desired location
        lang_data_path = os.path.join(self._download_path, 'usr', 'share', 'apertium')

        self._logger.info('Copying Language Data to Apertium')
        for directory in os.listdir(lang_data_path):
            source: str = str(os.path.join(lang_data_path, directory))
            destination: str = str(os.path.join(self._apertium_path, 'share', 'apertium', directory))
            copy_tree(source, destination)
            self._logger.info('%s -> %s', source, destination)

        shutil.rmtree(os.path.join(self._download_path, 'usr'))

    def _edit_modes(self) -> None:
        r"""The mode files need to be modified before being used on Windows System

        1. Replace /usr/share with %localappdata%\apertium-all-dev\share
        2. Replace "/" with "\" to make path compatible with Windows System
        """

        # List of Mode Files
        mode_path: str = str(os.path.join(self._apertium_path, 'share', 'apertium', 'modes'))
        for f in os.listdir(mode_path):
            if os.path.isfile(os.path.join(mode_path, f)) and f.endswith('.mode'):
                self._logger.info('Editing mode %s ', f)
                with open(os.path.join(mode_path, f)) as infile:
                    line = infile.read()

                contents = line.split(' ')
                # Editing mode file to be compatible with windows platform
                for i, t in enumerate(contents):
                    if len(t) > 2 and t[0] == "'" and t[1] == '/':
                        t = t.replace('/', os.sep)
                        t = t.replace(r'\usr', self._apertium_path)
                        contents[i] = t
                line = ' '.join(contents)
                with open(os.path.join(mode_path, f), 'w') as outfile:
                    outfile.write(line)
                    outfile.close()

    def install_apertium_base(self) -> None:
        """Installs Apertium-all-dev to %localappdata%"""

        apertium_windows = {
            'apertium-all-dev.zip': '/win64/nightly/apertium-all-dev.zip',
        }

        self._download_zip(apertium_windows, self._install_path)

    def install_apertium_module(self, language: str) -> None:
        self._download_package(language)
        self._edit_modes()

    def install_wrapper(self, swig_wrapper: str) -> None:
        # TODO: create installer for wrappers on windows
        pass


class Ubuntu:
    @staticmethod
    def _install_package_source() -> None:
        install_sh = 'install-nightly.sh' if nightly else 'install-release.sh'
        install_script_url = f'http://apertium.projectjj.com/apt/{install_sh}'
        with tempfile.NamedTemporaryFile('w') as install_script:
            urlretrieve(install_script_url, install_script.name)
            execute = subprocess.run(['sudo', 'bash', install_script.name])
            execute.check_returncode()

    @staticmethod
    def _download_package(package: str) -> None:
        command = ['sudo', 'apt-get', 'install', '-y', package]
        execute = subprocess.run(command)
        execute.check_returncode()

    @staticmethod
    def _rename_wrappers() -> None:
        wrapper_name = {
            'python3-apertium-core': '_apertium_core',
            'python3-apertium-lex-tools': '_apertium_lex_tools',
            'python3-cg3': '_constraint_grammar',
            'python3-lttoolbox': '_lttoolbox',
        }
        dist_package = '/usr/lib/python3/dist-packages'
        for wrapper in wrapper_name.values():
            for f in os.listdir(dist_package):
                if f.startswith(wrapper):
                    old_name = os.path.join(dist_package, f)
                    new_name = os.path.join(dist_package, '{}.so'.format(f.split('.')[0]))
                    if old_name != new_name:
                        subprocess.run(['sudo', 'mv', old_name, new_name])

    def install_apertium_module(self, language: str) -> None:
        self._download_package(language)

    def install_apertium_base(self) -> None:
        self._install_package_source()
        self._download_package('apertium-all-dev')

    def install_wrapper(self, swig_wrapper: str) -> None:
        self._download_package(swig_wrapper)
        self._rename_wrappers()


def get_installer() -> Union[Windows, Ubuntu]:
    system: str = platform.system()
    if system == 'Windows':
        return Windows()
    elif system == 'Linux':
        with open('/etc/os-release') as os_release:
            distro_name = os_release.readline().split('=')[-1].strip().replace('"', '')
        if distro_name == 'Ubuntu':
            return Ubuntu()
        else:
            raise apertium.InstallationNotSupported(distro_name)
    else:
        raise apertium.InstallationNotSupported(system)


def install_apertium() -> None:
    installer = get_installer()
    installer.install_apertium_base()


def install_module(module: str) -> None:
    apertium_module = 'apertium-{}'.format(module)
    installer: Union[Windows, Ubuntu] = get_installer()
    installer.install_apertium_module(apertium_module)


def install_wrapper(swig_wrapper: str) -> None:
    installer: Union[Windows, Ubuntu] = get_installer()
    installer.install_wrapper(swig_wrapper)


def install_apertium_linux() -> None:
    """
    Installs apertium-* packages on Linux Platforms
    """
    if platform.system() == 'Linux':
        install_module('anaphora')
