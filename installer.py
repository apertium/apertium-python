from urllib.request import urlretrieve
from zipfile import ZipFile
import os
from os import path
import platform
from distutils.dir_util import copy_tree
from shutil import rmtree


class Installer:

    def __init__(self, languages: tuple):
        self._install_path = os.getenv('LOCALAPPDATA')
        self._apertium_path = path.join(self._install_path, 'apertium-all-dev')
        self._temp_path = os.getenv('TEMP')
        self._download_path = path.join(self._temp_path, 'apertium_temp')
        self._language_link = 'http://apertium.projectjj.com/win32/nightly/data.php?zip={}'

        # Remove abandoned files from previous incomplete install
        if path.isdir(self._download_path):
            rmtree(self._download_path)

        os.mkdir(self._download_path)
        self._languages = languages

    @staticmethod
    def _download_zip(download_files: dict, download_dir, extract_path):
        for zip_name, zip_link in download_files.items():
            zip_download_path = path.join(download_dir, zip_name)
            urlretrieve(zip_link, filename=zip_download_path)
            print("{} download completed".format(zip_name))

            # Extact the zip
            zip_obj = ZipFile(zip_download_path, 'r')
            zip_obj.extractall(path=extract_path)
            zip_obj.close()
            print("Extraction completed")
            os.remove(zip_download_path)
            print("zip removed")

    def download_apertium_windows(self):
        """Installs Apertium-all-dev to %localappdata%"""

        download_dir = self._download_path
        extract_path = self._install_path

        apertium_windows = {
            'apertium-all-dev.zip':
                'http://apertium.projectjj.com/win64/nightly/apertium-all-dev.zip',
        }

        self._download_zip(apertium_windows, download_dir, extract_path)

    def download_language_data(self):
        """Installs Language Data to Apertium"""

        download_dir = self._download_path
        extract_path = self._download_path
        language_zip = dict()
        for curr_lang in self._languages:
            language_link = self._language_link.format(curr_lang)
            language_zip[curr_lang] = language_link

        self._download_zip(language_zip, download_dir, extract_path)

        # move the extracted files to desired location
        lang_data_path = path.join(self._download_path, 'usr', 'share', 'apertium')

        print("Copying Language Data to Apertium")
        for directory in os.listdir(lang_data_path):
            source = path.join(lang_data_path, directory)
            destination = path.join(self._apertium_path, 'share', 'apertium', directory)
            copy_tree(source, destination)
            print(source, '->', destination)

        rmtree(path.join(extract_path, 'usr'))

    def mode_editor(self):
        """The mode files need to be modified before being used on Windows System

        1. Replace /usr/share with %localappdata%\apertium-all-dev\share
        2. Replace '/' with '\' to make path compatible with Windows System
        3. Remove single quotes as it causes FileNotFound Error
        """

        # List of Mode Files
        mode_path = path.join(self._apertium_path, 'share', 'apertium', 'modes')
        only_files = [file for file in os.listdir(mode_path)
                      if path.isfile(path.join(mode_path, file)) and
                      'mode' in file]

        for file in only_files:
            print(f"Opening {file} for editing")
            infile = open(path.join(mode_path, file), 'r')
            line = infile.read()
            infile.close()
            contents = line.split(' ')
            # Editing mode file to be compatible with windows platform
            for index, t in enumerate(contents):
                if len(t) > 2 and t[0] == "'" and t[1] == "/":
                    t = t.replace('/', '\\')
                    t = t.replace(r'\usr', self._apertium_path)
                    # Instead of calling eng.autogen.bin, cmd calls 'eng.autogen.bin'
                    # Raising Error: 'File can't be opened error'
                    # Hence removing quotes from file
                    t = t.replace("'", '')
                    contents[index] = t
            line = ' '.join(contents)
            outfile = open(path.join(mode_path, file), 'w')
            outfile.write(line)
            outfile.close()
            print(f"Closing {file}")


def install_apertium_windows():
    # Download ApertiumWin64 and Move to %localappdata%

    if platform.system() == 'Windows':
        p = Installer(('apertium-eng', 'apertium-en-es'))
        p.download_apertium_windows()
        p.download_language_data()
        p.mode_editor()


if __name__ == '__main__':
    install_apertium_windows()
