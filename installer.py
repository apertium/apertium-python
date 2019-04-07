import logging
import os
import platform
import shutil
import tempfile
from distutils.dir_util import copy_tree
from urllib.request import urlretrieve
from zipfile import ZipFile

class Installer:

    base_link = "http://apertium.projectjj.com/{}{}"

    def __init__(self, languages):  # type: (Installer, list) -> None
        self._install_path = os.getenv('LOCALAPPDATA')
        self._apertium_path = os.path.join(self._install_path, 'apertium-all-dev')
        self._download_path = tempfile.mkdtemp()
        self._languages = languages
        logging.basicConfig(filename='installer.log', format='%(asctime)s %(message)s',
                            filemode='w', level=logging.DEBUG)
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)

    def _download_zip(self, download_files, download_dir, extract_path):
        # type: (Installer, dict, str, str) -> None

        for zip_name, zip_link in download_files.items():
            zip_download_path = os.path.join(download_dir, zip_name)
            urlretrieve(zip_link, filename=zip_download_path)
            self._logger.info('%s download completed', zip_name)

            # Extact the zip
            zip_obj = ZipFile(zip_download_path, 'r')
            zip_obj.extractall(path=extract_path)
            zip_obj.close()
            self._logger.info("%s Extraction completed", zip_name)
            os.remove(zip_download_path)
            self._logger.info("%s removed", zip_name)

    def download_apertium_windows(self):  # type: (Installer) -> None
        """Installs Apertium-all-dev to %localappdata%"""

        download_dir = self._download_path
        extract_path = self._install_path

        apertium_windows = {
            'apertium-all-dev.zip':
                'http://apertium.projectjj.com/win64/nightly/apertium-all-dev.zip',
        }

        self._download_zip(apertium_windows, download_dir, extract_path)

    def download_package(self):  # type: (Installer) -> None
        """Installs Language Data to Apertium"""

        zip_path = ""
        if platform.system() == 'Windows':
            zip_path = "win32/nightly/data.php?zip="
        download_dir = self._download_path
        extract_path = self._download_path
        language_zip = dict()
        for curr_lang in self._languages:
            language_link = Installer.base_link.format(zip_path, curr_lang)
            language_zip[curr_lang] = language_link

        self._download_zip(language_zip, download_dir, extract_path)

        # move the extracted files to desired location
        lang_data_path = os.path.join(self._download_path, 'usr', 'share', 'apertium')

        self._logger.info("Copying Language Data to Apertium")
        for directory in os.listdir(lang_data_path):
            source = os.path.join(lang_data_path, directory)
            destination = os.path.join(self._apertium_path, 'share', 'apertium', directory)
            copy_tree(source, destination)
            self._logger.info('%s -> %s', source, destination)

        shutil.rmtree(os.path.join(extract_path, 'usr'))

    def edit_modes(self):  # type: (Installer) -> None
        """The mode files need to be modified before being used on Windows System

        1. Replace /usr/share with %localappdata%\apertium-all-dev\share
        2. Replace '/' with '\' to make path compatible with Windows System
        3. Remove single quotes as it causes FileNotFound Error
        """

        # List of Mode Files
        mode_path = os.path.join(self._apertium_path, 'share', 'apertium', 'modes')
        only_files = [f for f in os.listdir(mode_path)
                      if os.path.isfile(os.path.join(mode_path, f)) and
                      'mode' in f]

        for file in only_files:
            self._logger.info("Editing mode %s ", file)
            with open(os.path.join(mode_path, file), 'r') as infile:
                line = infile.read()

            contents = line.split(' ')
            # Editing mode file to be compatible with windows platform
            for i, t in enumerate(contents):
                if len(t) > 2 and t[0] == "'" and t[1] == "/":
                    t = t.replace('/', '\\')
                    t = t.replace(r'\usr', self._apertium_path)
                    # Instead of calling eng.autogen.bin, cmd calls 'eng.autogen.bin'
                    # Raising Error: 'File can't be opened error'
                    # Hence removing quotes from file
                    t = t.replace("'", '')
                    contents[i] = t
            line = ' '.join(contents)
            with open(os.path.join(mode_path, file), 'w') as outfile:
                outfile.write(line)
                outfile.close()

def install_apertium_windows():
    """Download ApertiumWin64 and Move to %localappdata%"""

    if platform.system() == 'Windows':
        p = Installer(['apertium-eng', 'apertium-en-es'])
        p.download_apertium_windows()
        p.download_package()
        p.edit_modes()
