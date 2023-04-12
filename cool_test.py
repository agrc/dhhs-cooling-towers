#!/usr/bin/env python
# * coding: utf8 *
"""
test_cool.py
A module that contains tests for the project module.
"""

from pathlib import Path

import cool

root = Path(__file__).parent / "test-data"


def test_download_tiles():
    tiles = cool.download_tiles('198263', '394029')

    assert len(tiles) == 4


def test_build_mosaic_image():
    col = '198263'
    row = '394029'
    tiles = cool.download_tiles(col, row)

    mosaic = cool.build_mosaic_image(tiles, col, row, None)

    assert mosaic.shape == (512, 512, 3)


def test_detect_towers():
    file_name = root / "mosaic_198263_394029.jpg"

    results = cool.detect_towers(file_name).pandas().xyxy[0]

    print(len(results.index))

    assert results.empty is False
    assert len(results.index) > 0 is True