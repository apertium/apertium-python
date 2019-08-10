#!/usr/bin/env bash
set -xe

sudo apt-get install -y cmake libboost-dev libicu-dev swig build-essential python3-setuptools

git clone -b swig --depth 1 https://github.com/Vaydheesh/cg3.git
pushd cg3
cmake -DENABLE_PYTHON_BINDINGS:BOOL=ON .
cd python
make -j2
python3 setup.py install
popd
