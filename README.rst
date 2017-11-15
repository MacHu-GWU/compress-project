.. image:: https://travis-ci.org/MacHu-GWU/compress-project.svg?branch=master
    :target: https://travis-ci.org/MacHu-GWU/compress-project?branch=master

.. image:: https://codecov.io/gh/MacHu-GWU/compress-project/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/MacHu-GWU/compress-project

.. image:: https://img.shields.io/pypi/v/compress.svg
    :target: https://pypi.python.org/pypi/compress

.. image:: https://img.shields.io/pypi/l/compress.svg
    :target: https://pypi.python.org/pypi/compress

.. image:: https://img.shields.io/pypi/pyversions/compress.svg
    :target: https://pypi.python.org/pypi/compress

.. image:: https://img.shields.io/badge/Star_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/compress-project


Welcome to ``compress`` Documentation
==============================================================================

There's lots of mature data compression algorithm you can choose from, ``compress`` provides **normalized API** to use them and **switch between them**.

It supports:

- `zlib <https://docs.python.org/2/library/zlib.html>`_.
- `bz2 <https://docs.python.org/2/library/bz2.html>`_.
- `lzma <https://docs.python.org/3/library/lzma.html>`_, high compression ratio but slow (it's part of standard library after Python3.4, you can use `backports.lzma <https://pypi.python.org/pypi/backports.lzma>`_ for versions before that.)
- `pylzma <https://pypi.python.org/pypi/pylzma>`_, another implementation, faster in decompression than ``lzma``.
- `snappy <https://pypi.python.org/pypi/python-snappy>`_, from Google, lower compression ratio but super fast!
- `lz4 <https://pypi.python.org/pypi/lz4>`_, lower ratio, super fast!

.. note::

    some package are not installed along with ``compress``. Because **all of them needs C compiler**, you have to manually install them. If you have trouble installing C compiler for your OS, read `THIS TUTORIAL <https://github.com/MacHu-GWU/Setup-Environment-for-Python-Developer/blob/master/05-FAQ-Failed-to-compile-source-code.rst>`_.


Usage::

    >>> from compress import Compressor
    >>> c = Compressor()
    >>> c.use_zlib() # or use_bz2, use_lzma, use_lz4, use_snappy
    >>> c.compress(binary_data, zlib_level=9)
    >>> c.decompress(binary_data)

`This website <https://quixdb.github.io/squash-benchmark/>`_ provides comprehensive comparison and visualization. But how do you know **how it works on your own production environment?**.

``compress`` comes with a tool to run benchmark test for **All test case, All algorithm, All parameters**, and you will get informative stats about ratio, compress/decompress speed in ``.tab`` and ``ascii table`` format. Then You are able to visualize it in the way you preferred.

To run benchmark test, just::

    make up
    make benchmark

If you use **Windows** (doesn't have ``make`` command), this is the `SOLUTION <https://pygitrepo.readthedocs.io/index.html#software-environment-you-should-have>`_

Of course, you can **extend with your own test case** (`How to extend test case <https://github.com/MacHu-GWU/compress-project/blob/master/benchmark/README.rst>`_).


Quick Links
------------------------------------------------------------------------------

- .. image:: https://img.shields.io/badge/Link-Document-red.svg
      :target: https://compress.readthedocs.io/index.html

- .. image:: https://img.shields.io/badge/Link-API_Reference_and_Source_Code-red.svg
      :target: https://compress.readthedocs.io/py-modindex.html

- .. image:: https://img.shields.io/badge/Link-Install-red.svg
      :target: `install`_

- .. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/MacHu-GWU/compress-project

- .. image:: https://img.shields.io/badge/Link-Submit_Issue_and_Feature_Request-blue.svg
      :target: https://github.com/MacHu-GWU/compress-project/issues

- .. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.python.org/pypi/compress#downloads


.. _install:

Install
------------------------------------------------------------------------------

``compress`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install compress

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade compress

.. note::

    to install lzma, snappy, lz4 for python, it may requires gcc comiler. If you are using Windows,

