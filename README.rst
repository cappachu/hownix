
hownix: find and understand *nix commands 
====================================================

hownix makes it easy to find and learn how to use linux/unix commands. If you're new to the linux or unix command line hownix can help you get started.

Inspired by Benjamin Gleitzman's howdoi, hownix searches for, parses and makes use of explainshell.com to describe command lines found in StackOverflow answers. 

Installation
------------
::

    pip install git+https://github.com/mtamrf/hownix.git

or

::

    python setup.py install


How To hownix
-------------

Use hownix by describing the task you intend to perform with a phrase. hownix should respond by displaying a sample command line with parameters and an explanation of the parameters used.


Examples
--------

::

    $ hownix copy file to remote computer

.. image:: https://raw.github.com/mtamrf/hownix/master/misc/scp.png

::

    $ hownix find in contents of file 

.. image:: https://raw.github.com/mtamrf/hownix/master/misc/grep.png


Improvements
------------
- suggest commonly co-used parameters 
- search through shell history for previously used commands



