#!/usr/bin/env bash
set -xe

sudo apt-get install -y swig build-essential python3-setuptools

git clone --depth 1 https://github.com/apertium/lttoolbox.git
cd lttoolbox
./autogen.sh --enable-python-bindings && make -j2
cd python
python3 setup.py install

git clone --depth 1 https://github.com/apertium/apertium-lex-tools.git
cd apertium-lex-tools
./autogen.sh --enable-python-bindings && make -j2
cd python
python3 setup.py install
