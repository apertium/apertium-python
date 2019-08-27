Installation
============

From PyPI
-----------

- Clone the project and perform `python setup.py install`


    pip install apertium-python

- For developers


    git clone https://github.com/apertium/apertium-python.git
    cd apertium-python
    python setup.py install
    pip install pipenv
    pipenv install --dev --system

Apertium packages can be installed from python interpreter as well
  - Install `apertium-all-dev`


    import apertium
    apertium.installer.install_apertium()

  - Install language packages


    import apertium
    apertium.installer.install_module('eng')
    apertium.installer.install_module('en-es')
