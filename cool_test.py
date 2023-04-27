#!/usr/bin/env python
# * coding: utf8 *
"""
cool_test.py
A module that contains tests for the project module.
"""

from pathlib import Path
from unittest import mock

import pytest
import requests

import cool

root = Path(__file__).parent / "test-data"


@mock.patch("cool.get_tile")
@mock.patch("cool._get_secrets")
def test_download_tiles_calls_get_tile_with_correct_urls(mock_get_secrets, mock_get_tile):
    mock_get_secrets.return_value = {"QUAD_WORD": "test_string"}

    tiles = cool.download_tiles("1", "2", None)

    assert len(tiles) == 4
    assert mock_get_tile.call_count == 4

    calls = [
        mock.call("https://discover.agrc.utah.gov/login/path/test_string/tiles/utah/20/1/2"),
        mock.call("https://discover.agrc.utah.gov/login/path/test_string/tiles/utah/20/2/2"),
        mock.call("https://discover.agrc.utah.gov/login/path/test_string/tiles/utah/20/1/3"),
        mock.call("https://discover.agrc.utah.gov/login/path/test_string/tiles/utah/20/2/3"),
    ]
    mock_get_tile.assert_has_calls(calls)


def test_build_mosaic_image():
    col = "1"
    row = "2"
    test_data = ["1_2", "2_2", "1_3", "2_3"]
    tiles = [(root / f"{name}.jpg").read_bytes() for name in test_data]

    expected_mosaic = cool.convert_to_cv2_image((root / f"1_2_mosaic.jpg").read_bytes())

    actual_mosaic = cool.build_mosaic_image(tiles, col, row, None)

    assert actual_mosaic.shape == (512, 512, 3)
    assert actual_mosaic[127, 127, 0] == expected_mosaic[127, 127, 0]
    assert actual_mosaic[127, 384, 1] == expected_mosaic[127, 384, 1]
    assert actual_mosaic[384, 127, 2] == expected_mosaic[384, 127, 2]
    assert actual_mosaic[384, 384, 1] == expected_mosaic[384, 384, 1]


@pytest.mark.parametrize("input,expected", [("1_2_mosaic.jpg", 10), ("no_towers.jpg", 0)])
def test_detect_towers_finds_correct_number_of_towers(input, expected):
    file_name = root / input

    results_df = cool.detect_towers(file_name).pandas().xyxy[0]

    assert len(results_df.index) == expected


@mock.patch("cool._get_retry_session")
def test_get_tile_bad_url(session_mock):
    response_mock = mock.Mock()
    response_mock.raise_for_status.return_value = mock.Mock(side_effect=requests.exceptions.RequestException)
    session_mock.get.return_value = response_mock

    url = f"https://fake_bad_url.madeup/198263/394029"
    response = cool.get_tile(url)

    assert response is None
