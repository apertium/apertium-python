#!/usr/bin/env bash
set -xe

sudo apt-get install -y cmake libboost-dev libicu-dev swig build-essential python3-setuptools

git clone --depth 1 https://github.com/apertium/apertium-lex-tools.git
pushd apertium-lex-tools
./autogen.sh --enable-python-bindings
cd python
make -j2
python3 setup.py install
popd

git clone --depth 1 https://github.com/apertium/apertium.git apertium-core
pushd apertium-core
./autogen.sh --enable-python-bindings
cd python
make -j2
python3 setup.py install
popd

git clone --depth 1 https://github.com/apertium/lttoolbox.git
pushd lttoolbox
./autogen.sh --enable-python-bindings
cd python
make -j2
python3 setup.py install
popd

git clone --depth 1 https://github.com/TinoDidriksen/cg3.git
pushd cg3
cmake -DENABLE_PYTHON_BINDINGS:BOOL=ON .
cd python
make -j2
python3 setup.py install
popd
