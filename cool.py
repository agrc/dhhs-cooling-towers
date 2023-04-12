#!/usr/bin/env python
# * coding: utf8 *
"""
DHHS Cooling Tower object detection
Cooling tower module containing methods
"""
import json
import logging
import math
from os import environ
from pathlib import Path
from time import perf_counter, sleep
from types import SimpleNamespace

import cv2
import google.cloud.logging
import google.cloud.storage
import mercantile
import numpy as np
import pyproj
import requests
import torch

if "PY_ENV" in environ and environ["PY_ENV"] == "production":
    LOGGING_CLIENT = google.cloud.logging.Client()
    STORAGE_CLIENT = google.cloud.storage.Client()

    LOGGING_CLIENT.setup_logging()

QUAD_WORD = None
MODEL = None
SECRETS = None


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
        return json.loads((secret_folder / 'secrets.json').read_text(encoding='utf-8'))

    raise FileNotFoundError('Secrets folder not found; secrets not loaded.')



def convert_to_cv2_image(image):
    """convert image (bytes) to a cv2 image object

    Args:
        image (bytes): The image (bytes) to convert

    Returns:
        cv2.Image: A cv2 image object
    """
   
    return cv2.imdecode(np.frombuffer(image, dtype=np.uint8), 1)  # 1 means flags=cv2.IMREAD_COLOR


def download_tiles(col, row):
    """downloads image at specified col/row and each neigbor to the right, down, and right-down,
    then converts them to cv2 images and returns the list
    Args:
        col (str): the column of the WMTS index for the tile of interest (top-left tile)
        row (str): the row of the WMTS index for the tile of interest (top-left tile)
    Returns:
        cv2_images (list): list of cv2 images
    """
    global SECRETS

    if SECRETS is None:
        logging.info("loading secrets")
        SECRETS = SimpleNamespace(**_get_secrets())

    BASE_URL = f"https://discover.agrc.utah.gov/login/path/{SECRETS.QUAD_WORD}/tiles/utah/20"
    col_num = int(col)
    row_num = int(row)

    #: download primary tile (top-left)
    img_1 = requests.get(f"{BASE_URL}/{col_num}/{row_num}").content
    #: dowload top-right tile
    img_2 = requests.get(f"{BASE_URL}/{col_num + 1}/{row_num}").content
    #: dowload bottom-left tile
    img_3 = requests.get(f"{BASE_URL}/{col_num}/{row_num + 1}").content
    #: dowload bottom-right tile
    img_4 = requests.get(f"{BASE_URL}/{col_num + 1}/{row_num + 1}").content
    if out_dir:
        if not out_dir.exists():
            out_dir.mkdir(parents=True)

        i = 0
        for tile in tile_list:
            img = convert_to_cv2_image(tile)
            logging.info("download is saving from %s", type(img))
            tile_outfile = out_dir / f"{col}_{row}_{i}.jpg"
            logging.info("saving to %s", tile_outfile)
            cv2.imwrite(str(tile_outfile), img)

            i += 1

        return tile_list

    else:
        logging.debug("no output directory provided")

        return tile_list


def build_mosaic_image(tiles, col, row, out_dir):
    """build a mosaic image from a list of cv2 images

    Args:
        images (list): list of cv2 images to mosaic together
        col (str): the column of the WMTS index for the tile of interest (top-left tile)
        row (str): the row of the WMTS index for the tile of interest (top-left tile)
        out_dir (Path): location to save the result

    Returns:
        mosaic_image (np.ndarray): composite mosaic of smaller images
    """

    tile_name = f"{col}_{row}"

    if tiles is None or len(tiles) == 0:
        logging.info("no images to mosaic for %s", tile_name)

        return np.array(None)

    #: Set up parameters for images, mosaic, number of cols/rows (every image will be 256x256)
    tile_width = 256
    number_columns = 2
    number_rows = 2

    #: Build mosaic image with white background
    total_height = tile_width * number_rows
    total_width = tile_width * number_columns

    logging.info("mosaicking images for %s", tile_name)

    mosaic_image = np.zeros((total_height, total_width, 3), dtype=np.uint8)
    mosaic_image[:, :] = (255, 255, 255)

    i = 0
    for tile in tiles:
        #: convert from bytes to cv2
        img = convert_to_cv2_image(tile)
        #: add image into the mosaic
        row_start = (math.floor(i / number_columns)) * tile_width
        col_start = (i % number_columns) * tile_width
        mosaic_image[row_start : row_start + tile_width, col_start : col_start + tile_width] = img

        i += 1

    if out_dir:
        if not out_dir.exists():
            out_dir.mkdir(parents=True)

        mosaic_outfile = out_dir / f"{tile_name}.jpg"
        logging.debug("saving to %s", mosaic_outfile)
        cv2.imwrite(str(mosaic_outfile), mosaic_image)

        return mosaic_image

    else:
        logging.debug("no output directory provided")

        return mosaic_image


def load_pytorch_model():
    """load pytorch model with tower scout weights

    Args:
        None

    Returns:
        pytorch model: model ready for scanning
    """
    model_weight_path = Path(__file__).parent / "tower_scout" / "xl_250_best.pt"
    yolov5_path = Path(__file__).parent / "yolov5"
    model = torch.hub.load(str(yolov5_path), "custom", path=str(model_weight_path), source="local")
    #: if statements (check that .pt file exists, folders, etc.)

    return model


def get_model():
    """gets pytorch model using logic to ensure it's only loaded once

    Args:
        None

    Returns:
        model: loaded pytorch model ready for use
    """
    global MODEL
    if MODEL is None:
        logging.info("loading pytorch model")
        MODEL = load_pytorch_model()

    return MODEL


def detect_towers(image):
    """run pytorch model with tower scout weight on an image to detect cooling towers

    Args:
        image (obj): Path object to local image file or np.ndarray object of in-memory file

    Returns:
        result (obj): pytorch result object
    """
    towerscout_model = get_model()
        
    # if isinstance(image, Path):
    #     logging.info('working with a Path')
    #     pil_image = Image.open(image)
    # elif isinstance(image, np.ndarray):
    #     logging.info('working with a numpy array')
    #     pil_image = Image.fromarray(image)

    logging.info('working with %s', type(image))

    scan_start = perf_counter()
    results = towerscout_model(image)
    logging.info('time to scan image: %s',  format_time(perf_counter() - scan_start))

    results.save()

    return results


def parse_results(results, col, row):
    """parse detection results and calculate coordinates

    Args:
        results_df (dataframe): dataframe with results from pytorch model
        col (str): the column of the WMTS index for the tile of interest (top-left tile)
        row (str): the row of the WMTS index for the tile of interest (top-left tile)

    Returns:
        results_df (dataframe): results dataframe with additional columns that were calculated
    """
    results_df = results.pandas().xyxy[0]  #:0 gets the dataframe, otherwise it would be a list

    #: check for empty dataframe
    if results_df.empty:
        logging.info("empty dataframe, no cooling towers detected")

        return results_df

    zoom_level = 20

    #: get upper-left coordinates of the primary tile (upper-left tile)
    tile = mercantile.ul(int(col), int(row), zoom_level)

    #: calculate centroid in pixels
    results_df["x_centroid_px"] = (results_df["xmin"] + results_df["xmax"]) / 2
    results_df["y_centroid_px"] = (results_df["ymin"] + results_df["ymax"]) / 2

    #: project tile coords to web mercator (3857)
    wgs84 = 4326
    web_mercator = 3857

    transformer = pyproj.Transformer.from_crs(pyproj.CRS.from_epsg(wgs84), pyproj.CRS.from_epsg(web_mercator), always_xy=True)
    x, y = transformer.transform(tile.lng, tile.lat)

    #: calculate centroid x/y coords in web mercator
    meters_per_pixel = 0.1492910708688
    results_df["x_centroid_3857"] = x + results_df["x_centroid_px"] * meters_per_pixel
    results_df["y_centroid_3857"] = y - results_df["y_centroid_px"] * meters_per_pixel

    return results_df


def format_time(seconds):
    """seconds: number
    returns a human-friendly string describing the amount of time
    """
    minute = 60.00
    hour = 60.00 * minute

    if seconds < 30:
        return f"{int(seconds * 1000)} ms"

    if seconds < 90:
        return f"{round(seconds, 2)} seconds"

    if seconds < 90 * minute:
        return f"{round(seconds / minute, 2)} minutes"

    return f"{round(seconds / hour, 2)} hours"
