Apertium+Python Architecture and Module Design
==============================================



Overview
--------

Apertium+Python is a project that mainly aims at bringing Apertium features available in Python across a wide range of platforms.

The implementation of the current version uses the `subprocess` module in python to make appropriate calls to apertium commands.
Usage details can be found :doc:`here <./usage_details>`




The Main Modules
----------------


.. autoclass:: apertium.Analyzer
    :members:

.. autoclass:: apertium.Generator
    :members:

.. autoclass:: apertium.Translator
    :members:

.. automodule:: apertium.update_modes
    :members:
