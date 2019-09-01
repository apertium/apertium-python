Installation
============

From PyPI
-----------

- Install from PyPI by running
```
pip install apertium-python
```

- For developers, `pipenv` can be used to install the development dependencies and enter a shell with them:
```
pip install pipenv
pipenv install --dev
pipenv shell
```

Apertium packages can be installed from python interpreter as well
  - Install `apertium-all-dev`
```python
import apertium
apertium.installer.install_apertium()
```

  - Install language packages
```python
import apertium
apertium.installer.install_module('eng')
apertium.installer.install_module('en-es')
```
