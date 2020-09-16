#!/bin/sh

# Replace kaz-tat.automorf.bin with stable version
wget 'https://apertium.projectjj.com/win32/release/data.php?deb=apertium-kaz-tat' -O apertium-kaz-tat.deb
ar -x apertium-kaz-tat.deb && tar -xvf data.tar.xz
sudo mv -f ./usr/share/apertium/apertium-kaz-tat/kaz-tat.automorf.bin /usr/share/apertium/apertium-kaz-tat/kaz-tat.automorf.bin
