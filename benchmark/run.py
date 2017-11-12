#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script run benchmark on several popular dataset, you will get informative
stats about ratio, compress/decompress speed in `.tab` and `ascii table` format.
You are able to visualize it in the way you preferred.

Inspired by: https://quixdb.github.io/squash-benchmark/

Usage:

    Do ``pip install -r requirements-benchmark.txt`` before you run this.
"""

from __future__ import division
import sys
import json
import shutil
import timeit
import attr
import pandas as pd

pd.set_option("display.width", 160)

from pandas_mate.util import ascii_table
from sfm.timer import timeit_wrapper
from pathlib_mate.pathlib import Path
from pathlib_mate.mate import repr_data_size
from compress import CompressAlgorithms

from helper import Spider, create_logger

spider = Spider()
logger = create_logger()
pwd = Path(__file__).parent


@attr.s
class Result(object):
    """
    Single test result schema.

    :param file_number: number of files processed.
    :param before_size: total size of files in bytes.
    :param after_size: total size of compressed files in bytes.
    :param compress_time: average total process time for compression.
    :param decompress_time: average total process time for decompression.
    """
    file_number = attr.ib(default=0)
    before_size = attr.ib(default=0)
    after_size = attr.ib(default=0)
    compress_time = attr.ib(default=0)
    decompress_time = attr.ib(default=0)


@attr.s
class Row(object):
    """
    Benchmark stats DataFrame Row Schema.
    """
    case = attr.ib(default=None)
    case_description = attr.ib(default=None)
    algo = attr.ib(default=None)
    com_params_json = attr.ib(default=None)
    decom_params_json = attr.ib(default=None)
    file_number = attr.ib(default=None)
    before_size = attr.ib(default=None)
    before_size_text = attr.ib(default=None)
    after_size = attr.ib(default=None)
    after_size_text = attr.ib(default=None)
    compress_ratio = attr.ib(default=None)
    compress_ratio_text = attr.ib(default=None)
    compress_time = attr.ib(default=None)
    decompress_time = attr.ib(default=None)
    compress_speed = attr.ib(default=None)
    compress_speed_text = attr.ib(default=None)
    decompress_speed = attr.ib(default=None)
    decompress_speed_text = attr.ib(default=None)


columns = [f.name for f in attr.fields(Row)]

REPEAT_TIMES = 10


class Case(object):
    description = None

    @property
    def dirpath(self):
        p = pwd.append_parts(self.__class__.__name__)
        try:
            p.mkdir()
        except:
            pass
        return p

    @property
    def size(self):
        return self.dirpath.dirsize

    def setup(self):
        raise NotImplementedError

    def teardown(self):
        shutil.rmtree(self.dirpath.abspath)
        pass

    def run_benchmark_with_specified_algorithm(self,
                                               algo,
                                               repeat_times):
        df = list()
        for com_params, decom_params in algo.all_params:
            logger.info("Params %s, %s ..." % (com_params, decom_params), 2)

            res = Result()
            for p in self.dirpath.select_file():
                logger.info("File '%s' ..." % p.basename, 3)

                res.file_number += 1

                data = p.read_bytes()
                res.before_size += sys.getsizeof(data)
                compressed_data = algo.compress(data, **com_params)
                res.after_size += sys.getsizeof(compressed_data)

                res.compress_time += timeit.timeit(
                    timeit_wrapper(algo.compress, data, **com_params),
                    number=repeat_times,
                ) / repeat_times

                res.decompress_time += timeit.timeit(
                    timeit_wrapper(algo.decompress, compressed_data,
                                   **decom_params),
                    number=repeat_times,
                ) / repeat_times

            row = Row()
            row.case = self.__class__.__name__
            row.case_description = self.description
            row.algo = algo.__name__
            row.com_params_json = json.dumps(com_params)
            row.decom_params_json = json.dumps(decom_params)
            row.file_number = res.file_number
            row.before_size = res.before_size
            row.after_size = res.after_size
            row.compress_time = res.compress_time
            row.decompress_time = res.decompress_time
            df.append(attr.astuple(row))

        df = pd.DataFrame(df, columns=columns)
        df.compress_ratio = df.before_size / df.after_size
        df.compress_ratio_text = df.compress_ratio.apply(
            lambda ratio: "%.2f" % ratio)
        df.before_size_text = df.before_size.apply(repr_data_size)
        df.after_size_text = df.after_size.apply(repr_data_size)
        df.compress_speed = df.before_size / df.compress_time
        df.compress_speed_text = df.compress_speed.apply(
            lambda speed: "%s/S" % repr_data_size(speed))
        df.decompress_speed = df.after_size / df.decompress_time
        df.decompress_speed_text = df.decompress_speed.apply(
            lambda speed: "%s/S" % repr_data_size(speed))

        return df

    def _run_benchmark(self,
                       repeat_times=REPEAT_TIMES):

        dfs = list()
        logger.info("Case '%s' ..." % self.__class__.__name__)
        for algo in CompressAlgorithms._algorithm_class_list:
            logger.info("Algo '%s' ..." % algo.__name__, 1)
            df = self.run_benchmark_with_specified_algorithm(
                algo, repeat_times=repeat_times)
            dfs.append(df)
        return pd.concat(dfs)

    def run_benchmark(self):
        return self._run_benchmark()


class C1_Alice29(Case):
    description = "http://corpus.canterbury.ac.nz/descriptions/cantrbry/text.html"

    def setup(self):
        file_path = self.dirpath.append_parts("alice29.txt")
        if not file_path.exists():
            url = "https://s3.amazonaws.com/www.wbh-doc.com/FileHost/compress-project-test-data/alice29.txt"
            content = spider.get_content(url)
            file_path.write_bytes(content)


class C2_Dickens(Case):
    description = "http://sun.aei.polsl.pl/~sdeor/index.php?page=silesia"  # dickens

    def setup(self):
        file_path = self.dirpath.append_parts("dickens.txt")
        if not file_path.exists():
            url = "https://s3.amazonaws.com/www.wbh-doc.com/FileHost/compress-project-test-data/dickens.txt"
            content = spider.get_content(url)
            file_path.write_bytes(content)

    def run_benchmark(self):
        return self._run_benchmark(repeat_times=3)


class C3_Enwik8(Case):
    description = "http://www.mattmahoney.net/dc/textdata.html"  # enwik8.zip

    def setup(self):
        file_path = self.dirpath.append_parts("enwik8.txt")
        if not file_path.exists():
            url = "https://s3.amazonaws.com/www.wbh-doc.com/FileHost/compress-project-test-data/enwik8.txt"
            content = spider.get_content(url)
            file_path.write_bytes(content)

    def run_benchmark(self):
        return self._run_benchmark(repeat_times=1)


class C4_Bliss(Case):
    description = "https://en.wikipedia.org/wiki/Bliss_(image)"

    def setup(self):
        file_path = self.dirpath.append_parts("windows_xp_bliss-wide.jpg")
        if not file_path.exists():
            url = "https://s3.amazonaws.com/www.wbh-doc.com/FileHost/compress-project-test-data/windows_xp_bliss-wide.jpg"
            content = spider.get_content(url)
            file_path.write_bytes(content)

    def run_benchmark(self):
        return self._run_benchmark(repeat_times=3)


class C5_OSDB(Case):
    description = "https://sourceforge.net/projects/osdb/"  # osdb

    def setup(self):
        file_path = self.dirpath.append_parts("osdb")
        if not file_path.exists():
            url = "https://s3.amazonaws.com/www.wbh-doc.com/FileHost/compress-project-test-data/osdb"
            content = spider.get_content(url)
            file_path.write_bytes(content)

    def run_benchmark(self):
        return self._run_benchmark(repeat_times=3)


def run():
    def select_informative_columns(df):
        return df[[
            "case", "algo", "com_params_json",
            "before_size_text",
            "compress_ratio_text", "compress_speed_text",
            "decompress_speed_text",
        ]]

    dfs = list()
    for klass in Case.__subclasses__():
        case = klass()
        case.setup()
        df = case.run_benchmark()
        dfs.append(df)

    df = pd.concat(dfs)
    df = select_informative_columns(df)

    df.to_csv("benchmark.tab", sep="\t", index=False)
    with open("benchmark.txt", "wb") as f:
        f.write(ascii_table(df).encode("utf-8"))


if __name__ == "__main__":
    run()
    spider.close()
