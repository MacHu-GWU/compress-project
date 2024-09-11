# -*- coding: utf-8 -*-

import sys
import json
import timeit
import dataclasses

import requests
from tabulate import tabulate
from diskcache import Cache
from pathlib_mate import PathCls as Path
from pathlib_mate.helper import repr_data_size

from compress.api import Algorithm, compress, decompress


dir_here = Path(__file__).absolute().parent
dir_cache = Path(dir_here, ".cache")
dir_log = Path(dir_here, ".log")

dir_cache.mkdir(exist_ok=True)
cache = Cache(str(dir_cache))

path_result = Path(dir_here, "result.txt")
REPEAT_TIME = 3


@dataclasses.dataclass
class Dataset:
    name: str = dataclasses.field()
    type: str = dataclasses.field()
    description: str = dataclasses.field()
    download_url: str = dataclasses.field()

    def get_data(self):
        if self.download_url in cache:
            return cache[self.download_url]
        else:
            content = requests.get(self.download_url).content
            cache[self.download_url] = content
            return content


@dataclasses.dataclass
class Case:
    algo: Algorithm = dataclasses.field()
    com_kwargs: dict = dataclasses.field(default_factory=dict)
    decom_kwargs: dict = dataclasses.field(default_factory=dict)

    def to_compress_kwargs(self):
        return dict(algo=case.algo, data=b, kwargs=case.com_kwargs)

    def to_decompress_kwargs(self):
        return dict(algo=case.algo, data=b, kwargs=case.decom_kwargs)


dataset_list = [
    Dataset(
        name="alice29",
        type="novel",
        description="http://corpus.canterbury.ac.nz/descriptions/cantrbry/text.html",
        download_url="https://github.com/MacHu-GWU/compress-project/releases/download/test-data/alice29.txt",
    ),
    Dataset(
        name="dickens",
        type="novel",
        description="http://sun.aei.polsl.pl/~sdeor/index.php?page=silesia",
        download_url="https://github.com/MacHu-GWU/compress-project/releases/download/test-data/dickens",
    ),
    Dataset(
        name="enwik8",
        type="english wikipedia",
        description="http://www.mattmahoney.net/dc/textdata.html",
        download_url="https://github.com/MacHu-GWU/compress-project/releases/download/test-data/enwik8",
    ),
    Dataset(
        name="bliss",
        type="image",
        description="https://en.wikipedia.org/wiki/Bliss_(image)",
        download_url="https://github.com/MacHu-GWU/compress-project/releases/download/test-data/windows-xp-bliss-4k-lu-1920x1080.jpg",
    ),
    Dataset(
        name="osdb",
        type="binary",
        description="https://sourceforge.net/projects/osdb/",
        download_url="https://github.com/MacHu-GWU/compress-project/releases/download/test-data/osdb-0.90.tar.gz",
    ),
]

case_list = [
    Case(algo=Algorithm.gzip, com_kwargs=dict(compresslevel=1)),
    Case(algo=Algorithm.gzip, com_kwargs=dict(compresslevel=5)),
    Case(algo=Algorithm.gzip, com_kwargs=dict(compresslevel=9)),
    Case(algo=Algorithm.bz2, com_kwargs=dict(compresslevel=1)),
    Case(algo=Algorithm.bz2, com_kwargs=dict(compresslevel=5)),
    Case(algo=Algorithm.bz2, com_kwargs=dict(compresslevel=9)),
    Case(algo=Algorithm.lzma),
    Case(algo=Algorithm.snappy),
    Case(algo=Algorithm.lz4),
    Case(algo=Algorithm.lz4),
    Case(algo=Algorithm.lz4),
    Case(algo=Algorithm.zstd, com_kwargs=dict(level_or_option=1)),
    Case(algo=Algorithm.zstd, com_kwargs=dict(level_or_option=10)),
    Case(algo=Algorithm.zstd, com_kwargs=dict(level_or_option=20)),
]


@dataclasses.dataclass
class Record:
    pass


def timeit_wrapper(func, *args, **kwargs):
    """
    Wrapper function makes ``timeit.timeit`` easier to use.

    Usage::

        >>> import timeit
        >>> def func(*args, **kwargs):
        ...     pass # a function you want to measure
        >>> timeit.timeit(timeit_wrapper(func, *args, **kwargs), number=10)
        0.000153
    """

    def wrapper():
        return func(*args, **kwargs)

    return wrapper


record_list = list()
for dataset in dataset_list:
    b = dataset.get_data()
    before_size = sys.getsizeof(b)
    before_size_rep = repr_data_size(before_size)
    for case in case_list:
        print(f"work on {dataset = }, {case = }")
        b_compressed = compress(**case.to_compress_kwargs())
        after_size = sys.getsizeof(b_compressed)
        after_size_rep = repr_data_size(after_size)
        compress_ratio = after_size / before_size
        total_elapsed = timeit.timeit(
            timeit_wrapper(compress, **case.to_compress_kwargs()),
            number=REPEAT_TIME,
        )
        elapsed = total_elapsed / REPEAT_TIME
        record = {
            "dataset_name": dataset.name,
            "dataset_type": dataset.type,
            "dataset_size": before_size,
            "dataset_size_rep": before_size_rep,
            "algo_name": case.algo.name,
            "com_kwargs": json.dumps(case.com_kwargs),
            "after_size": after_size,
            "after_size_rep": after_size_rep,
            "compress_ratio": "%.6f" % compress_ratio,
            "elapsed": "%.6f" % elapsed,
        }
        record_list.append(list(record.values()))

headers = [
    "dataset_name",
    "dataset_type",
    "dataset_size",
    "dataset_size_rep",
    "algo_name",
    "com_kwargs",
    "after_size",
    "after_size_rep",
    "compress_ratio",
    "elapsed",
]
s = tabulate(
    tabular_data=record_list,
    headers=headers,
    tablefmt="psql",
)
path_result.write_text(s)
print(s)
