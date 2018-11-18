=================
Apertium + Python
=================

.. toctree::
   :maxdepth: 2

Introduction
------------

- The code-base is in development for the Gsoc '18 project called **Apertium API in Python**.
- The Apertium core modules are written in C++.
- This project is an attempt to make the Apertium modules available in python, which because of it's simplicity is more appealing to users.

About the Exisiting Code Base
-----------------------------

- The exisiting code base has the subprocess implementation of the basic functions of Apertium.
- A branch called the ``windows`` has the implementation for the ``windows`` support and will soon be available on master. Detailed instructions can be found `here <https://gist.github.com/arghyatiger/c8aab476022158f4bdb3dbe45308cdb4/>`_

Usage of library
----------------

Analysis
^^^^^^^^

Performing Morphological Analysis

Method 1: One can create ``Analyzer`` objects on which the ``analyze()`` method can be run::

    In [1]: import apertium
    In [2]: a = apertium.Analyzer('en')
    In [3]: a.analyze('cats')
    Out[3]: [cats/cat<n><pl>, ./.<sent>]

Method 2: Alternatively, the library provides an option to directly run the ``analyze()`` method::

    In [1]: import apertium
    In [2]: apertium.analyze('en', 'cats')
    Out[2]: cats/cat<n><pl>

Generation
^^^^^^^^^^

Performing Morphological Generation

Method 1: Just like the ``Analyzer``, One can create ``Generator`` objects on which the ``generate()`` method can be run::

    In [1]: import apertium
    In [2]: g = apertium.Generator('en')
    In [3]: g.generate('^cat<n><pl>$')
    Out[3]: 'cats'

Method 2: Running ``generate()`` directly::

    In [1]: import apertium
    In [2]: apertium.generate('en', '^cat<n><pl>$')
    Out[2]: 'cats'

Installing more modes from other language data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One can also install modes by providing the path to the lang-data using this simple function::

    In [1]: import apertium
    In [2]: apertium.append_pair_path('..')

Translation
^^^^^^^^^^^

Performing Translations::

    In [1]: import apertium
    In [2]: t = apertium.Translator('eng', 'spa')
    In [3]: t.translate('cats')
    Out[3]: 'Gatos'

=============
Documentation
=============

Analysis
--------

.. automodule:: apertium.analysis
    :members:
    :undoc-members:
    :private-members:

Generation
----------

.. automodule:: apertium.generation
    :members:
    :undoc-members:
    :private-members:

Translation
-----------

.. automodule:: apertium.translation
    :members:
    :undoc-members:
    :private-members:

Mode Search Script
------------------

.. automodule:: apertium.mode_search
    :members:
    :undoc-members:
    :private-members:

Utils Script
------------

.. automodule:: apertium.utils
    :members:
    :undoc-members:
    :private-members:

==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`