# -*- coding: utf-8 -*-

from compress import api


def test():
    _ = api


if __name__ == "__main__":
    from compress.tests import run_cov_test

    run_cov_test(__file__, "compress.api", preview=False)
