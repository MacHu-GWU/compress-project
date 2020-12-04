Compression library in Python benchmark test
==============================================================================

+-------------------------------------+-------------+------------------------------+------------------------+---------+
| dataset                             | algorithm   | params                       | elapsed                |   ratio |
|-------------------------------------+-------------+------------------------------+------------------------+---------|
| alice29, novel, 148.56 KB           | gzip        | {'compresslevel': 1}         | 0.022725 (repeat 10)   |    0.43 |
| alice29, novel, 148.56 KB           | gzip        | {'compresslevel': 5}         | 0.057526 (repeat 10)   |    0.37 |
| alice29, novel, 148.56 KB           | gzip        | {'compresslevel': 9}         | 0.113307 (repeat 10)   |    0.36 |
| alice29, novel, 148.56 KB           | bz2         | {'compresslevel': 1}         | 0.116749 (repeat 10)   |    0.3  |
| alice29, novel, 148.56 KB           | bz2         | {'compresslevel': 5}         | 0.121670 (repeat 10)   |    0.28 |
| alice29, novel, 148.56 KB           | bz2         | {'compresslevel': 9}         | 0.117076 (repeat 10)   |    0.28 |
| alice29, novel, 148.56 KB           | lzma        | {}                           | 0.468186 (repeat 10)   |    0.32 |
| alice29, novel, 148.56 KB           | snappy      | {}                           | 0.007404 (repeat 10)   |    0.58 |
| alice29, novel, 148.56 KB           | lz4         | {'mode': 'default'}          | 0.005362 (repeat 10)   |    0.58 |
| alice29, novel, 148.56 KB           | lz4         | {'mode': 'fast'}             | 0.005028 (repeat 10)   |    0.58 |
| alice29, novel, 148.56 KB           | lz4         | {'mode': 'high_compression'} | 0.066831 (repeat 10)   |    0.42 |
| dickens, novel, 9.72 MB             | gzip        | {'compresslevel': 1}         | 1.634476 (repeat 10)   |    0.45 |
| dickens, novel, 9.72 MB             | gzip        | {'compresslevel': 5}         | 4.198512 (repeat 10)   |    0.39 |
| dickens, novel, 9.72 MB             | gzip        | {'compresslevel': 9}         | 9.007514 (repeat 10)   |    0.38 |
| dickens, novel, 9.72 MB             | bz2         | {'compresslevel': 1}         | 7.635132 (repeat 10)   |    0.32 |
| dickens, novel, 9.72 MB             | bz2         | {'compresslevel': 5}         | 8.071931 (repeat 10)   |    0.29 |
| dickens, novel, 9.72 MB             | bz2         | {'compresslevel': 9}         | 8.404518 (repeat 10)   |    0.27 |
| dickens, novel, 9.72 MB             | lzma        | {}                           | 80.086134 (repeat 10)  |    0.28 |
| dickens, novel, 9.72 MB             | snappy      | {}                           | 0.325667 (repeat 10)   |    0.62 |
| dickens, novel, 9.72 MB             | lz4         | {'mode': 'default'}          | 0.337634 (repeat 10)   |    0.63 |
| dickens, novel, 9.72 MB             | lz4         | {'mode': 'fast'}             | 0.326261 (repeat 10)   |    0.63 |
| dickens, novel, 9.72 MB             | lz4         | {'mode': 'high_compression'} | 6.123727 (repeat 10)   |    0.43 |
| enwik8, english wikipedia, 95.37 MB | gzip        | {'compresslevel': 1}         | 19.037774 (repeat 10)  |    0.42 |
| enwik8, english wikipedia, 95.37 MB | gzip        | {'compresslevel': 5}         | 39.144063 (repeat 10)  |    0.37 |
| enwik8, english wikipedia, 95.37 MB | gzip        | {'compresslevel': 9}         | 63.691684 (repeat 10)  |    0.36 |
| enwik8, english wikipedia, 95.37 MB | bz2         | {'compresslevel': 1}         | 80.745755 (repeat 10)  |    0.33 |
| enwik8, english wikipedia, 95.37 MB | bz2         | {'compresslevel': 5}         | 79.982168 (repeat 10)  |    0.3  |
| enwik8, english wikipedia, 95.37 MB | bz2         | {'compresslevel': 9}         | 85.719857 (repeat 10)  |    0.29 |
| enwik8, english wikipedia, 95.37 MB | lzma        | {}                           | 736.169837 (repeat 10) |    0.26 |
| enwik8, english wikipedia, 95.37 MB | snappy      | {}                           | 3.019703 (repeat 10)   |    0.57 |
| enwik8, english wikipedia, 95.37 MB | lz4         | {'mode': 'default'}          | 2.889396 (repeat 10)   |    0.57 |
| enwik8, english wikipedia, 95.37 MB | lz4         | {'mode': 'fast'}             | 2.919022 (repeat 10)   |    0.57 |
| enwik8, english wikipedia, 95.37 MB | lz4         | {'mode': 'high_compression'} | 36.539009 (repeat 10)  |    0.42 |
| bliss, image, 1.00 MB               | gzip        | {'compresslevel': 1}         | 0.345056 (repeat 10)   |    0.99 |
| bliss, image, 1.00 MB               | gzip        | {'compresslevel': 5}         | 0.324869 (repeat 10)   |    0.99 |
| bliss, image, 1.00 MB               | gzip        | {'compresslevel': 9}         | 0.328419 (repeat 10)   |    0.99 |
| bliss, image, 1.00 MB               | bz2         | {'compresslevel': 1}         | 1.216205 (repeat 10)   |    0.99 |
| bliss, image, 1.00 MB               | bz2         | {'compresslevel': 5}         | 1.173680 (repeat 10)   |    0.99 |
| bliss, image, 1.00 MB               | bz2         | {'compresslevel': 9}         | 1.254775 (repeat 10)   |    0.99 |
| bliss, image, 1.00 MB               | lzma        | {}                           | 2.459851 (repeat 10)   |    0.99 |
| bliss, image, 1.00 MB               | snappy      | {}                           | 0.001389 (repeat 10)   |    0.99 |
| bliss, image, 1.00 MB               | lz4         | {'mode': 'default'}          | 0.002873 (repeat 10)   |    0.99 |
| bliss, image, 1.00 MB               | lz4         | {'mode': 'fast'}             | 0.002742 (repeat 10)   |    0.99 |
| bliss, image, 1.00 MB               | lz4         | {'mode': 'high_compression'} | 0.278232 (repeat 10)   |    0.99 |
| osdb, binary, 9.62 MB               | gzip        | {'compresslevel': 1}         | 1.552075 (repeat 10)   |    0.4  |
| osdb, binary, 9.62 MB               | gzip        | {'compresslevel': 5}         | 2.603250 (repeat 10)   |    0.37 |
| osdb, binary, 9.62 MB               | gzip        | {'compresslevel': 9}         | 4.407402 (repeat 10)   |    0.36 |
| osdb, binary, 9.62 MB               | bz2         | {'compresslevel': 1}         | 7.276421 (repeat 10)   |    0.37 |
| osdb, binary, 9.62 MB               | bz2         | {'compresslevel': 5}         | 7.052809 (repeat 10)   |    0.29 |
| osdb, binary, 9.62 MB               | bz2         | {'compresslevel': 9}         | 7.416336 (repeat 10)   |    0.28 |
| osdb, binary, 9.62 MB               | lzma        | {}                           | 46.210920 (repeat 10)  |    0.28 |
| osdb, binary, 9.62 MB               | snappy      | {}                           | 0.197421 (repeat 10)   |    0.54 |
| osdb, binary, 9.62 MB               | lz4         | {'mode': 'default'}          | 0.231357 (repeat 10)   |    0.52 |
| osdb, binary, 9.62 MB               | lz4         | {'mode': 'fast'}             | 0.220226 (repeat 10)   |    0.52 |
| osdb, binary, 9.62 MB               | lz4         | {'mode': 'high_compression'} | 2.307575 (repeat 10)   |    0.39 |
+-------------------------------------+-------------+------------------------------+------------------------+---------+