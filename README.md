# Apertium + Python

[![Travis Build Status](https://travis-ci.com/apertium/apertium-python.svg?branch=master)](https://travis-ci.com/apertium/apertium-python)
[![Appveyor Build status](https://ci.appveyor.com/api/projects/status/sesdinoy4cw2p1tk/branch/master?svg=true)](https://ci.appveyor.com/project/sushain97/apertium-python/branch/master)
[![ReadTheDocs Docs Status](https://readthedocs.org/projects/apertium-python/badge)](https://readthedocs.org/projects/apertium-python)
[![Coverage Status](https://coveralls.io/repos/github/apertium/apertium-python/badge.svg?branch=master)](https://coveralls.io/github/apertium/apertium-python?branch=master)

## Introduction
- The code-base is in development for the GSoC '19 project called **Apertium API in Python**
- The Apertium core modules are written in C++.
- This project is an attempt to make the Apertium modules available in python, which because of it's simplicity is more appealing to users.

## About the Exisiting Code Base
- The exisiting code base has the subprocess and swig wrapper implementation of the basic functions of Apertium. 

## ToDo
- ToDo is present in form of issues https://github.com/apertium/apertium-python/issues

## Usage of library

- For multiple invocations `Method 1` is more performant, as the dictionary needs to be loaded only once.

### Analysis
Performing Morphological Analysis

Method 1: Create `Analyzer` object and call its `analyze()` method.
```
In [1]: import apertium
In [2]: a = apertium.Analyzer('en')
In [3]: a.analyze('cats')
Out[3]: [cats/cat<n><pl>, ./.<sent>]
```
Method 2: Calling `analyze` method directly.
```
In [1]: import apertium
In [2]: apertium.analyze('en', 'cats')
Out[2]: cats/cat<n><pl>
```

### Generation
Performing Morphological Generation

Method 1:  Create `Generator` and call its `generate()` method.
``` 
In [1]: import apertium
In [2]: g = apertium.Generator('en')
In [3]: g.generate('^cat<n><pl>$')
Out[3]: 'cats'
```
Method 2: Calling `generate()` directly.
``` 
In [1]: import apertium
In [2]: apertium.generate('en', '^cat<n><pl>$')
Out[2]: 'cats'
```

### Installing more modes from other language data
One can also install modes by providing the path to the lang-data using this simple function
```
In [1]: import apertium
In [2]: apertium.append_pair_path('..')
```

### Tagger
Method 1:  Create `Tagger` object and call its `tag` method.
```
In [1]: import apertium
In [2]: tagger = apertium.Tagger('eng')
In [3]: tagger.tag('cats')
Out[3]: [cats/cat<n><pl>]
```
Method 2: Calling `tag()` directly.
```
In [1]: import apertium
In [2]: apertium.tag('en', 'cats')
Out[2]: [cats/cat<n><pl>]
```

### Translation
Method 1:  Create `Translator` object and call its `translate()` method.
```
In [1]: import apertium
In [2]: t = apertium.Translator('eng', 'spa')
In [3]: t.translate('cats')
Out[3]: 'Gatos'
```
Method 2: Calling `translate()` directly.
```
In [1]: import apertium
In [2]: apertium.translate('en', 'spa', 'cats')
Out[2]: 'Gatos'
```