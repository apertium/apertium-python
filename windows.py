import urllib.request
import zipfile
import os
from subprocess import PIPE, Popen
from distutils.dir_util import copy_tree
import shutil

download_url_lang_data = "http://apertium.projectjj.com/win32/nightly/data.php?deb={}"
download_array = ["apertium-eng", "apertium-en-es"]

print("Downloading apertium-all dev")
urllib.request.urlretrieve( "http://apertium.projectjj.com/win64/nightly/apertium-all-dev.zip", "apertium-all-dev.zip")   # Downloading apertium-all-dev
print("Download done")
print("Extracting Apertium-All-Dev")
zip_ref = zipfile.ZipFile("apertium-all-dev.zip", 'r')  # Extracting the apertium-all-dev
zip_ref.extractall()
zip_ref.close()
print("Extraction completed")
print("removing the zip")
os.remove("apertium-all-dev.zip")
print("zip removed")

for i in download_array:
	print("downloading landata", i)
	urllib.request.urlretrieve(download_url_lang_data.format(i), "{}.deb".format(i))  # Downloading language data
	print("dowload done")
	
	print("Extracting the .deb files now")
	p = Popen(['7z', 'x', "{}.deb".format(i) ], stdout=PIPE, shell='true')
	p.communicate()
	print("Dowload done")
	
	print("Extracting the data.tar")
	p1 = Popen(['7z', 'x', 'data.tar'], stdout=PIPE, shell='true')
	p1.communicate()
	print("Extraction of data.tar done")
	
	print("removing the data.tar")
	os.remove("data.tar")
	print("removed data.tar")
	
	print("copying the modes")
	copy_tree(r'.\usr\share\apertium\modes', r'.\apertium-all-dev\share\apertium\modes')
	print("modes copied")
	
	print("copying the other lang files")
	copy_tree(r'.\usr\share\apertium\{}'.format(i), r'apertium-all-dev\share\apertium')
	print("lang files copied")
	
	print("Deleting the current ./usr")
	shutil.rmtree(r'usr')
	print("Current usr  directory deleted")
	
	print("Deleting the debian packages")
	os.remove("{}.deb".format(i))
	print("Deleted the current debian package")
