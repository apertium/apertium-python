Usage
=====

Analysis
--------

Performing Morphological Analysis

Method 1: One can create `Analyzer` objects on which the `analyze()` method can be run.


    In [1]: import apertium
    In [2]: a = apertium.Analyzer('en')
    In [3]: a.analyze('cats')
    Out[3]: [cats/cat<n><pl>, ./.<sent>]


Method 2: Alternatively, the library provides an option to directly run the `analyze()` method.


    In [1]: import apertium
    In [2]: apertium.analyze('en', 'cats')
    Out[2]: cats/cat<n><pl>


Generation
----------

Performing Morphological Generation

Method 1: Just like the `Analyzer`, One can create `Generator` objects on which the `generate()` method can be run::


    In [1]: import apertium
    In [2]: g = apertium.Generator('en')
    In [3]: g.generate('-cat<n><pl>$')
    Out[3]: 'cats'


Method 2: Running `generate()` directly::

    In [1]: import apertium
    In [2]: apertium.generate('en', '-cat<n><pl>$')
    Out[2]: 'cats'

Installing more modes from other language data
----------------------------------------------

One can also install modes by providing the path to the lang-data using this simple function::

    In [1]: import apertium
    In [2]: apertium.append_pair_path('..')

Translation
-----------

Performing Translations::

    In [1]: import apertium
    In [2]: t = apertium.Translator('eng', 'spa')
    In [3]: t.translate('cats')
    Out[3]: 'Gatos'
