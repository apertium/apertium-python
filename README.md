# Apertium + Python

[![Travis Build Status](https://travis-ci.com/apertium/apertium-python.svg?branch=master)](https://travis-ci.com/apertium/apertium-python)
[![Appveyor Build status](https://ci.appveyor.com/api/projects/status/sesdinoy4cw2p1tk/branch/master?svg=true)](https://ci.appveyor.com/project/sushain97/apertium-python/branch/master)
[![ReadTheDocs Docs Status](https://readthedocs.org/projects/apertium-python/badge)](https://readthedocs.org/projects/apertium-python)
[![Coverage Status](https://coveralls.io/repos/github/apertium/apertium-python/badge.svg?branch=master)](https://coveralls.io/github/apertium/apertium-python?branch=master)

## Introduction
- The code-base is in development for the Gsoc '18 project called **Apertium API in Python**
- The Apertium core modules are written in C++.
- This project is an attempt to make the Apertium modules available in python, which because of it's simplicity is more appealing to users.

## About the Exisiting Code Base
- The exisiting code base has the subprocess implementation of the basic functions of Apertium. 
- A branch called the ```windows``` has the implementation for the ```windows``` support and will soon be available on master. Detailed instructions can be found [here](https://gist.github.com/arghyatiger/c8aab476022158f4bdb3dbe45308cdb4)

## Major things to do
- Subprocess implementation of the C++ functions in Apertium. To make the wrapper thinner.
- Other small issues can be found [here](https://github.com/apertium/apertium-python/issues)

## Usage of library

### Analysis
Performing Morphological Analysis

Method 1: One can create ```Analyzer``` objects on which ```analyze()``` function can be run.
```python
In [1]: import apertium
In [2]: a = apertium.Analyzer('en')
In [3]: a.analyze('cats')
Out[3]: [cats/cat<n><pl>, ./.<sent>]
```
Method 2: Alternatively, the library provides an option to directly run the ```analyze``` method.
```python
In [1]: import apertium
In [2]: apertium.analyze('en', 'cats')
Out[2]: cats/cat<n><pl>
```

### Generation
Performing Morphological Generation

Method 1:  Just like the ```Analyzer```, One can create ```Generator``` objects on which ```generate()``` function can be run.
```python 
In [1]: import apertium
In [2]: g = apertium.Generator('en')
In [3]: g.generate('^cat<n><pl>$')
Out[3]: 'cats'
```
Method 2: Running ```generate()``` directly.
```python 
In [1]: import apertium
In [2]: apertium.generate('en', '^cat<n><pl>$')
Out[2]: 'cats'
```

### Installing more modes from other language data
One can also install modes by providing the path to the lang-data using this simple function
```python
In [1]: import apertium
In [2]: apertium.append_pair_path('..')
```

### Translation
Performing Translations
```python
In [1]: import apertium
In [2]: t = apertium.Translator('eng', 'spa')
In [3]: t.translate('cats')
Out[3]: 'Gatos'
```
