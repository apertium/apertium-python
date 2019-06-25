#!/usr/bin/env bash
set -e

sudo apt-get install -y swig build-essential python3-setuptools
git clone https://github.com/apertium/lttoolbox.git
cd lttoolbox
./autogen.sh --enable-python-bindings && make
cd python
python3 setup.py install

git clone -b swig_wrapper https://github.com/Vaydheesh/apertium-lex-tools.git
cd apertium-lex-tools
./autogen.sh --enable-python-bindings && make
cd python
python3 setup.py install
