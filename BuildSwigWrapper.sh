#! /bin/bash
sudo apt-get install -y swig build-essential python3-setuptools
git clone -b swig_wrapper https://github.com/Vaydheesh/lttoolbox.git
cd lttoolbox || return
./autogen.sh && ./configure && make
cd python || return
python3 setup.py install