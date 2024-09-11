
.. image:: https://readthedocs.org/projects/compress/badge/?version=latest
    :target: https://compress.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/compress-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/compress-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/compress-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/compress-project

.. image:: https://img.shields.io/pypi/v/compress.svg
    :target: https://pypi.python.org/pypi/compress

.. image:: https://img.shields.io/pypi/l/compress.svg
    :target: https://pypi.python.org/pypi/compress

.. image:: https://img.shields.io/pypi/pyversions/compress.svg
    :target: https://pypi.python.org/pypi/compress

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/compress-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/compress-project

------

.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://compress.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://compress.readthedocs.io/en/latest/py-modindex.html

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
.. image:: https://compress.readthedocs.io/en/latest/_static/compress-logo.png
    :target: https://compress.readthedocs.io/en/latest/

``compress`` provides a unified interface for various mature data compression algorithms. It supports algorithms from both the Python Standard Library and the community, offering a range of options for different compression needs.

**Supported Algorithms**

**From Python Standard library**

- `zlib <https://docs.python.org/2/library/zlib.html>`_.
- `bz2 <https://docs.python.org/2/library/bz2.html>`_.
- `lzma <https://docs.python.org/3/library/lzma.html>`_, high compression ratio but slow.

**From Community (Additional Library Required)**

- `snappy <https://pypi.python.org/pypi/python-snappy>`_, from Google, lower compression ratio but super fast! (on MacOS, you need to install it via ``brew install snappy``, on Ubuntu, you need ``sudo apt-get install libsnappy-dev``.
- `lz4 <https://pypi.python.org/pypi/lz4>`_, lower ratio, super fast!
- `pyzstd <https://pypi.python.org/pypi/pyzstd>`_, very fast!

Note: Community libraries are not installed by default with compress. To include them, use:

.. code-block:: bash

    pip install compress[lz4,snappy,zstd]

These libraries require a C compiler. If you encounter issues installing the C compiler for your OS, refer to `this tutorial <https://github.com/MacHu-GWU/Setup-Environment-for-Python-Developer/blob/master/05-FAQ-Failed-to-compile-source-code.rst>`_.

**Usage Example**

.. code-block:: python

    import sys
    import compress.api as compress

    data = ("hello world" * 1000).encode("utf-8")
    print(f"before: {sys.getsizeof(data)}")

    data_compressed = compress.compress(
        algo=compress.Algorithm.gzip,
        data=data,
        kwargs={"compresslevel": 9},
    )
    print(f"after: {sys.getsizeof(data_compressed)}")

**Benchmark**

`This website <https://quixdb.github.io/squash-benchmark/>`_ provides comprehensive comparison and visualization. But how do you know **how it works on your own production environment?**.

``compress`` comes with a tool to run benchmark test for **All test case, All algorithm, All parameters**, and you will get informative stats about ratio, compress/decompress speed in ``ascii table`` format. Then You are able to visualize it in the way you preferred.

To run benchmark test, just do:

.. code-block:: bash

    pip install -r requirements-benchmark.txt
    python ./benchmark/run_benchmark.py

Then you can find the result at `benchmark/result.txt </Users/sanhehu/Documents/GitHub/compress-project/benchmark/result.txt>`_.


.. _install:

Install
------------------------------------------------------------------------------

``compress`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install compress

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade compress
