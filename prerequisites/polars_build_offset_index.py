# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 09:21:49 2023

@author: eneemann
"""

import gc
import time
from pathlib import Path

import mercantile
import numpy as np
import polars as pl

#: start timer and print start time
start_time = time.time()
readable_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("The script start time is {}".format(readable_start))

#: set up variables
out_dir = r'C:\Users\eneemann\Desktop\Neemann\cooling_towers\boundary'

#: Utah WMTS tiling info
x_min = 192093
x_max = 206656
y_min = 389243
y_max = 408141
x_span = 14563
y_span = 18898

#: total tiles = 14563 * 18898 = 275,211,574
#: index will be built with every other tile
#: 275,211,574 / 4 = 68,802,893 points in the index
#: create list to hold values from min to max
x_list = np.arange(x_min, x_max, 2)
y_list = np.arange(y_min, y_max, 2)

print("Building x/y indices ...")
index_time = time.time()
x_indices = []
y_indices = []
for x in x_list:
    for y in y_list:
        x_indices.append(x)
        y_indices.append(y)

print("Time elapsed building indices: {:.3f}s".format(time.time() - index_time))

polars_time = time.time()
dfpl = pl.DataFrame({'col': x_indices, 'row': y_indices})

dfpl = dfpl.with_columns([
    pl.struct(['col', 'row']).apply(lambda r: mercantile.ul(r['col'], r['row'], 20).lng).alias("lon"),
    pl.struct(['col', 'row']).apply(lambda r: mercantile.ul(r['col'], r['row'], 20).lat).alias("lat"),
    ])

print("Time elapsed building dataframe: {:.3f}s".format(time.time() - polars_time))

out_file = Path(out_dir).joinpath("imagery_index.parquet")
write_time = time.time()
dfpl.write_parquet(out_file)
print("Time elapsed writing to zstd compressed parquet file: {:.3f}s".format(time.time() - write_time))

del dfpl
gc.collect()


print("Script shutting down ...")
#: stop timer and print end time
readable_end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("The script end time is {}".format(readable_end))
print("Time elapsed: {:.2f}s".format(time.time() - start_time))
