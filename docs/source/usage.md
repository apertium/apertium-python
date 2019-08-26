Usage
=====

- For multiple invocations `Method 1` is more performant, as the dictionary needs to be loaded only once.

Analysis
--------

Performing Morphological Analysis

- Method 1: Create an `Analyzer` object and call its `analyze` method.


    In [1]: import apertium
    In [2]: a = apertium.Analyzer('en')
    In [3]: a.analyze('cats')
    Out[3]: [cats/cat<n><pl>, ./.<sent>]


- Method 2: Calling `analyze()` directly.


    In [1]: import apertium
    In [2]: apertium.analyze('en', 'cats')
    Out[2]: cats/cat<n><pl>


Generation
----------

Performing Morphological Generation

- Method 1:  Create a `Generator` object and call its `generate` method.


    In [1]: import apertium
    In [2]: g = apertium.Generator('en')
    In [3]: g.generate('-cat<n><pl>$')
    Out[3]: 'cats'


- Method 2: Calling `generate()` directly.

    In [1]: import apertium
    In [2]: apertium.generate('en', '-cat<n><pl>$')
    Out[2]: 'cats'

Installing more modes from other language data
----------------------------------------------

One can also install modes by providing the path to the lang-data using this simple function::

    In [1]: import apertium
    In [2]: apertium.append_pair_path('..')

Tagger
-----------

Performing Tagging::

- Method 1:  Create a `Tagger` object and call its `tag` method.


    In [1]: import apertium
    In [2]: tagger = apertium.Tagger('eng')
    In [3]: tagger.tag('cats')
    Out[3]: [cats/cat<n><pl>]


- Method 2: Calling `tag()` directly.


    In [1]: import apertium
    In [2]: apertium.tag('en', 'cats')
    Out[2]: [cats/cat<n><pl>]

Translation
-----------

Performing Translations::

- Method 1:  Create a `Translator` object and call its `translate` method.


    In [1]: import apertium
    In [2]: t = apertium.Translator('eng', 'spa')
    In [3]: t.translate('cats')
    Out[3]: 'Gatos'


- Method 2: Calling `translate()` directly.


    In [1]: import apertium
    In [2]: apertium.translate('en', 'spa', 'cats')
    Out[2]: 'Gatos'
