Usage of library
================

|
|

Analysis
--------

Performing Morphological Analysis

* Method 1: One can create `Analyzer` objects on which `analyze()` function can be run::

	>>> import apertium

	>>> a = apertium.Analyzer('en')

	>>> a.analyze('cats')

	>>> [cats/cat<n><pl>, ./.<sent>]

* Method 2: Alternatively, the library provides an option to directly run the `analyze` method.::

	>>> import apertium

	>>> apertium.analyze('en', 'cats')

	>>> cats/cat<n><pl>

|
|

Generation
----------

Performing Morphological Generation

* Method 1:  Just like the `Analyzer`, One can create `Generator` objects on which `generate()` function can be run.::

	>>> import apertium

	>>> g = apertium.Generator('en')

	>>> g.generate('^cat<n><pl>$')

	>>> 'cats'

* Method 2: Running `generate()` directly.

	>>> import apertium

	>>> apertium.generate('en', '^cat<n><pl>$')

	>>> 'cats'

|
|

Installing more modes from other language data
----------------------------------------------

* One can also install modes by providing the path to the lang-data using this simple function::

	>>> import apertium

	>>> apertium.append_pair_path('..')

|
|

Translation
-----------

Performing Translations

* Method 1:

	>>> import apertium

	>>> t = apertium.Translator('eng', 'spa')

	>>> t.translate('cats')

	>>> 'Gatos'

* Method 2:

	>>> import apertium

	>>> apertium.translate('eng', 'spa', 'I love you')

	>>> 'Te quieres'
