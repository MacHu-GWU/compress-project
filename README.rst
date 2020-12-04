
.. image:: https://github.com/MacHu-GWU/compress-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/compress-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/compress-project/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/compress-project

.. image:: https://img.shields.io/pypi/v/compress.svg
    :target: https://pypi.python.org/pypi/compress

.. image:: https://img.shields.io/pypi/l/compress.svg
    :target: https://pypi.python.org/pypi/compress

.. image:: https://img.shields.io/pypi/pyversions/compress.svg
    :target: https://pypi.python.org/pypi/compress

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/compress-project

------


.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: http://compress.my-docs.com/index.html

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: http://compress.my-docs.com/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
    :target: http://compress.my-docs.com/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/compress-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/compress-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/compress-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/compress#files


Welcome to ``compress`` Documentation
==============================================================================

There's lots of mature data compression algorithm you can choose from, ``compress`` provides **normalized API** to use them and **switch between them**.

It supports:

From Python Standard library:

- `zlib <https://docs.python.org/2/library/zlib.html>`_.
- `bz2 <https://docs.python.org/2/library/bz2.html>`_.
- `lzma <https://docs.python.org/3/library/lzma.html>`_, high compression ratio but slow

From Community (Additional Library Required):

- `snappy <https://pypi.python.org/pypi/python-snappy>`_, from Google, lower compression ratio but super fast! (on MacOS, you need to install it via ``brew install snappy``, on Ubuntu, you need ``sudo apt-get install libsnappy-dev``.
- `lz4 <https://pypi.python.org/pypi/lz4>`_, lower ratio, super fast!

.. note::

    some package are not installed along with ``compress``. Because **all of them needs C compiler**, you have to manually install them. If you have trouble installing C compiler for your OS, read `THIS TUTORIAL <https://github.com/MacHu-GWU/Setup-Environment-for-Python-Developer/blob/master/05-FAQ-Failed-to-compile-source-code.rst>`_.

Usage::

    >>> from compress import Compressor
    >>> binary_data = ("hello world! " * 100).encode("utf-8")
    >>> c = Compressor()
    >>> c.use_gzip() # or use_bz2, use_lzma, use_lz4, use_snappy
    >>> c.compress(binary_data, zlib_level=9)
    >>> c.decompress(binary_data)


Other API for lazy developer::

    >>> import compress
    >>> compress.compress_bytes_to_bytes
    >>> compress.compress_str_to_bytes
    >>> compress.compress_bytes_to_b64str # compress, and returns b64 encoded str
    >>> compress.compress_str_to_b64str # compress string and returns b64 encoded str

    >>> compress.decompress_bytes_to_bytes # inverse of compress_bytes_to_bytes
    >>> compress.decompress_bytes_to_str # inverse of compress_str_to_bytes
    >>> compress.decompress_b64str_to_bytes # inverse of compress_bytes_to_b64str
    >>> compress.decompress_b64str_to_str # inverse of compress_str_to_b64str

        compress_bytes_to_bytes, compress_str_to_bytes,
    compress_bytes_to_b64str, compress_str_to_b64str,
    decompress_bytes_to_bytes, decompress_bytes_to_str,
    decompress_b64str_to_bytes, decompress_b64str_to_str,


`This website <https://quixdb.github.io/squash-benchmark/>`_ provides comprehensive comparison and visualization. But how do you know **how it works on your own production environment?**.

``compress`` comes with a tool to run benchmark test for **All test case, All algorithm, All parameters**, and you will get informative stats about ratio, compress/decompress speed in ``.tab`` and ``ascii table`` format. Then You are able to visualize it in the way you preferred.

To run benchmark test, just::

    $ pip install -r requirements-benchmark.txt
    $ python ./benchmark/run.py


.. _install:

Install
------------------------------------------------------------------------------

``compress`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install compress

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade compress