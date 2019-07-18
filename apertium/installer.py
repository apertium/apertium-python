from distutils.dir_util import copy_tree
import logging
import os
import platform
import shutil
import subprocess
import tempfile
from typing import Optional
from urllib.request import urlretrieve
from zipfile import ZipFile

import distro


class Windows:
    """Download ApertiumWin64 and Move to %localappdata%"""
    base_link = 'http://apertium.projectjj.com/{}'

    def __init__(self, languages: list) -> None:
        self._install_path = os.getenv('LOCALAPPDATA')
        self._apertium_path = os.path.join(self._install_path, 'apertium-all-dev')
        self._download_path = tempfile.mkdtemp()
        self._languages = languages
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)

    def _download_zips(self, download_files: dict, extract_path: Optional[str]) -> None:
        for zip_name, zip_link in download_files.items():
            zip_download_path = os.path.join(self._download_path, zip_name)
            urlretrieve(Windows.base_link.format(zip_link), filename=zip_download_path)
            self._logger.info('%s download completed', zip_name)

            # Extract the zip
            with ZipFile(zip_download_path) as zip_file:
                zip_file.extractall(path=extract_path)
            self._logger.info('%s Extraction completed', zip_name)
            os.remove(zip_download_path)
            self._logger.info('%s removed', zip_name)

    def _download_apertium_windows(self) -> None:
        """Installs Apertium-all-dev to %localappdata%"""

        apertium_windows = {
            'apertium-all-dev.zip': '/win64/nightly/apertium-all-dev.zip',
        }

        self._download_zips(apertium_windows, self._install_path)

    def _download_package(self) -> None:
        """Installs Language Data to Apertium"""

        if platform.system() == 'Windows':
            zip_path = 'win32/nightly/data.php?zip='
        else:
            raise ValueError('Installation for {} is not supported'.format(platform.system()))
        language_zip = {}
        for curr_lang in self._languages:
            language_zip[curr_lang] = zip_path + curr_lang

        self._download_zips(language_zip, self._download_path)

        # move the extracted files to desired location
        lang_data_path = os.path.join(self._download_path, 'usr', 'share', 'apertium')

        self._logger.info('Copying Language Data to Apertium')
        for directory in os.listdir(lang_data_path):
            source = os.path.join(lang_data_path, directory)
            destination = os.path.join(self._apertium_path, 'share', 'apertium', directory)
            copy_tree(source, destination)
            self._logger.info('%s -> %s', source, destination)

        shutil.rmtree(os.path.join(self._download_path, 'usr'))

    def _edit_modes(self) -> None:
        r"""The mode files need to be modified before being used on Windows System

        1. Replace /usr/share with %localappdata%\apertium-all-dev\share
        2. Replace "/" with "\" to make path compatible with Windows System
        """

        # List of Mode Files
        mode_path = os.path.join(self._apertium_path, 'share', 'apertium', 'modes')
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
        self._download_apertium_windows()

    def install_apertium_language(self) -> None:
        self._download_package()
        self._edit_modes()


class Ubuntu:
    def __init__(self, languages: list) -> None:
        self._languages = languages
        init_script = 'wget http://apertium.projectjj.com/apt/install-nightly.sh -O - | sudo bash'
        subprocess.run(init_script, shell=True, check=True)
        self._languages = languages

    @staticmethod
    def _download_package(packages: list) -> None:
        command = 'sudo apt-get -f --allow-unauthenticated install {}'
        for package in packages:
            subprocess.run(command.format(package), shell=True, check=True)

    def install_apertium_language(self) -> None:
        install_packages = self._languages
        self._download_package(install_packages)

    def install_apertium_base(self) -> None:
        self._download_package(['apertium-all-dev'])


def install_language_pack(languages: list = None, install_base: bool = False) -> None:
    if languages is None:
        languages = ['apertium-eng', 'apertium-en-es']
    apertium_installer = None
    if platform.system() == 'Windows':
        apertium_installer = Windows(languages)
    elif distro.name() == 'Ubuntu':
        apertium_installer = Ubuntu(languages)
    else:
        raise ValueError('Installation on {} not supported'.format(distro.name()))
    if install_base:
        apertium_installer.install_apertium_base()
    apertium_installer.install_apertium_language()
