Windows Support for Apertium+Python
===================================

There are several dependencies and the process of getting Apertium+Python to work on windows is a bit complicated.

A proper installation method is in development for Windows. But for developers who would like to use the following software,
this document should provide sufficient guidance on doing so.

|
|

STEPS:
------
|

* Clone the repository for Apertium+Python [https://github.com/apertium/apertium-python]


* Download apertium-all-dev.zip [http://apertium.projectjj.com/win64/nightly/]


* Extract and set ``apertium-all-dev/bin`` folder to the PATH from ``cmd`` using ``SET PATH=%PATH%%cd%\apertium-all-dev\bin``


* Download .deb language data file from [http://apertium.projectjj.com/win32/nightly/data.php]


* Extract using 7z (Download this and install in windows system and set the path to 7z to the PATH)


* Extract the ``data.tar`` file obtained and copy the both the folders (modes\ and lang-pair\) to \apertium-all-dev\share\apertium


* All ``.mode`` files in the modes\ folder need to be updated with appropriate paths.


* Ideally all the path like structures need to be altered to replace ``usr\share`` with ``.\apertium-all-dev\share\``


* There exists a script in the repository called ``windows.py`` which ideally does all of the following and downloads ``apertium-eng`` and ``apertium-en-es`` but that can be easily modified.

|
|

COMPILATION:
------------

|

The language data have been downloaded but need to be compiled before usage.

For the following, ``lt-comp`` command has to be run on the ``.autogen.bin`` and ``automorph.bin`` files which
exist in the ``language-data`` folder.

More information about compilation using ``lt-comp`` can be found here[http://wiki.apertium.org/wiki/Compiling_dictionaries]