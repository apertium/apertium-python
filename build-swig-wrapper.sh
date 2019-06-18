#!/usr/bin/env bash
sudo apt-get install -y swig build-essential python3-setuptools
git clone -b swig_wrapper https://github.com/Vaydheesh/lttoolbox.git
cd lttoolbox || set -e
./autogen.sh --enable-python-bindings && make
cd python || set -e
python3 setup.py install