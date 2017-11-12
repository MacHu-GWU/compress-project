#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import requests
from pathlib_mate import Path
from diskcache import Cache
from loggerFactory import SingleFileLogger

cache_dir = Path(__file__).change(new_basename=".cache")
log_dir = Path(__file__).change(new_basename=".log")
try:
    log_dir.mkdir()
except:
    pass


class Spider(object):
    def __init__(self, directory=cache_dir.abspath, expire=24 * 3600):
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


def create_logger():
    fname = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.txt")
    logger = SingleFileLogger(path=log_dir.append_parts(fname).abspath)
    return logger


if __name__ == "__main__":
    import zlib

    # url = "https://raw.githubusercontent.com/google/snappy/master/testdata/alice29.txt"
    # with Spider() as spider:
    #     data = spider.get_content(url)
    #     compressed_data = zlib.compress(data)

    create_logger()
