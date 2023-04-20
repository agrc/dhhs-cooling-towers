#!/usr/bin/env python
# * coding: utf8 *
"""
test_cool.py
A module that contains tests for the project module.
"""

import json
from pathlib import Path
from types import SimpleNamespace

import cool

root = Path(__file__).parent / "test-data"


def _get_secrets():
    """load secrets for use in the program

    Args:
        None

    Returns:
        dict: A dictionary containing the secrets
    """
    secret_folder = Path("/secrets")

    #: Try to get the secrets from the Cloud Function mount point
    if secret_folder.exists():
        return json.loads(Path("/secrets/app/secrets.json").read_text(encoding="utf-8"))

    #: Otherwise, try to load a local copy for local development
    secret_folder = Path(__file__).parent / "secrets"
    if secret_folder.exists():
        return json.loads((secret_folder / "secrets.json").read_text(encoding="utf-8"))

    raise FileNotFoundError("Secrets folder not found; secrets not loaded.")


SECRETS = SimpleNamespace(**_get_secrets())
BASE_URL = f"https://discover.agrc.utah.gov/login/path/{SECRETS.QUAD_WORD}/tiles/utah/20"


def test_download_tiles():
    tiles = cool.download_tiles("198263", "394029", None)

    assert len(tiles) == 4


def test_build_mosaic_image():
    col = "198263"
    row = "394029"
    tiles = cool.download_tiles(col, row, None)

    mosaic = cool.build_mosaic_image(tiles, col, row, None)

    assert mosaic.shape == (512, 512, 3)


def test_detect_towers():
    file_name = root / "mosaic_198263_394029.jpg"

    results_df = cool.detect_towers(file_name).pandas().xyxy[0]

    print(f'length of results df is: {len(results_df.index)}')

    assert results_df.empty is False
    assert(len(results_df.index) > 0) is True


def test_get_tile_good_request():
    
    url = f"{BASE_URL}/{198263}/{394029}"
    print(url)
    response = cool.get_tile(url)

    assert response is not None
    assert response.status_code == 200


def test_get_tile_malformed_request():
    
    url = f"{BASE_URL}/bad_{198263}/{394029}"
    print(url)
    response = cool.get_tile(url)

    assert response is None


def test_get_tile_bad_url():
    
    url = f"https://fake_bad_url.madeup/198263/394029"
    print(url)
    response = cool.get_tile(url)

    assert response is None
