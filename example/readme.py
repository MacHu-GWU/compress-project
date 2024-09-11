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
