# Apertium + Python

[![Travis Build Status](https://travis-ci.org/apertium/apertium-python.svg)](https://travis-ci.org/apertium/apertium-python)
[![Appveyor Build status](https://ci.appveyor.com/api/projects/status/sesdinoy4cw2p1tk/branch/master?svg=true)](https://ci.appveyor.com/project/sushain97/apertium-python/branch/master)
[![Coverage Status](https://coveralls.io/repos/github/apertium/apertium-python/badge.svg?branch=master)](https://coveralls.io/github/apertium/apertium-python?branch=master)

## Introduction
- The code-base is in development for the Gsoc '18 project called **Apertium API in Python**
- The Apertium core modules are written in C++.
- This project is an attempt to make the Apertium modules available in python, which because of it's simplicity is more appealing to users.

## About the Code Base
- The development starts initially with a subprocess implementation of all the uses of Apertium, like Analysis, Generation, Translation etc. For which, code has been ported from [apertium-apy](https://github.com/apertium/apertium-apy "apertium-apy codebase")
- The second part of the project involves using SWIG to expose modules that require lower level functionality access.
- Which will be followed by a pip release.

## Usage of library

### Analysis
Performing Morphological Analysis
```python
In [1]: import apertium
In [2]: apertium.analyze('cats', 'en')
Out[2]: cats/cat<n><pl>
```
 
 ### Generation
 Performing Morphological Generation
  ```python 
In [1]: import apertium
In [2]: apertium.generate('cat<n><pl>', 'en')
Out[2]: 'cats'
 ```
 
### Installing more modes from other language data
One can also install modes by providing the path to the lang-data using this simple function
```python
In [1]: import apertium as a
In [2]: a.append_pair_path('..')
```
