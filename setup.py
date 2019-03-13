from os import path
from setuptools import setup


setup(
    name='apertium-app',
    version='1.0',
    license = 'MIT',
    description='this is a windows installer for apertium',
    long_description=open(path.join(path.abspath(path.dirname(__file__)), 'README.md')).read(),
    long_description_content_type='text/markdown; charset=UTF-8',
    keywords='apertium',
    author='James Sandy',
    author_email='mondaysandy3@gmail.com',
    url='https://github.com/apertium/apertium',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    
)

