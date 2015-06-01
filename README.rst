
hownix: find and understand *nix commands 
====================================================

hownix makes it easy to find and learn how to use linux/unix commands. If you're new to the linux or unix command line hownix can help you get started.

Inspired by howdoi
explain shell


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

    $ hownix copy remote file 

.. image:: https://raw.github.com/matamrf/hownix/master/misc/scp.png


Improvements
------------
- suggest commonly co-used parameters 
- search through shell history for previously used commands



