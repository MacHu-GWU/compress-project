# -*- coding: utf-8 -*-

from datetime import datetime

import sys
import timeit
import requests
import yaml
from diskcache import Cache
from loggerFactory import SingleFileLogger
from pathlib_mate import PathCls as Path
from pathlib_mate.helper import repr_data_size
from compress import Compressor
from sfm.timer import timeit_wrapper
from tabulate import tabulate

HERE = Path(__file__).absolute().parent
CACHE_DIR = Path(HERE, ".cache")
LOG_DIR = Path(HERE, ".log")

CACHE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

REPEAT_TIME = 10


def create_logger():
    fname = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.txt")
    logger = SingleFileLogger(path=Path(LOG_DIR, fname).abspath)
    return logger


class Spider:
    """
    disk cache backed spider
    """

    def __init__(self, directory=CACHE_DIR.abspath, expire=24 * 3600):
        self.cache = Cache(directory)
        self.expire = expire

    def close(self):
        self.cache.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_content(self, url):
        if url in self.cache:
            return self.cache[url]
        else:
            content = requests.get(url).content
            self.cache[url] = content
            return content


config = yaml.safe_load(Path(HERE, "config.yml").read_text(encoding="utf-8"))
compressor = Compressor()
spider = Spider()
logger = create_logger()

df = list()

# test each algorithm on same data set
for dataset_config in config["dataset"]:

    dataset_name, dataset_type, download_url = dataset_config["name"], dataset_config["type"], dataset_config["download_url"]
    content = spider.get_content(url=download_url)
    before_size = sys.getsizeof(content)
    before_size_rep = repr_data_size(before_size)

    for algo_config in config["algorithms"]:
        algo_name, params = algo_config["name"], algo_config["params"]

        # use algorithm
        getattr(compressor, f"use_{algo_name}")()

        for kwargs in params:

            logger.info(f"testing {dataset_name}, {algo_name}, {str(kwargs)} ...")

            compressed_content = compressor.compress(content, **kwargs)
            after_size = sys.getsizeof(compressed_content)

            elapsed = timeit.timeit(
                timeit_wrapper(
                    compressor.compress, content, **kwargs
                ),
                number=REPEAT_TIME
            )

            compress_ratio = after_size / before_size

            row = (
                f"{dataset_name}, {dataset_type}, {before_size_rep}",
                algo_name,
                str(kwargs),
                "%.6f (repeat %s)" % (elapsed, REPEAT_TIME),
                "%.2f" % compress_ratio,
            )

            df.append(row)

print(tabulate(
    df,
    headers="dataset,algorithm,params,elapsed,ratio".split(","),
    tablefmt="psql",
))



