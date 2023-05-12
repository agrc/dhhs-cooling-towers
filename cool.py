#!/usr/bin/env python
# * coding: utf8 *
"""
DHHS Cooling Tower object detection
Cooling tower module containing methods
"""
import json
import logging
import math
from os import environ, getenv
from pathlib import Path
from time import perf_counter
from types import SimpleNamespace

import cv2
import google.cloud.bigquery as bigquery
import google.cloud.logging
import google.cloud.storage
import mercantile
import numpy as np
import pyproj
import requests
import torch
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

if "PY_ENV" in environ and environ["PY_ENV"] == "production":
    logging.info("setting up production environment")
    LOGGING_CLIENT = google.cloud.logging.Client()
    STORAGE_CLIENT = google.cloud.storage.Client()
    BIGQUERY_CLIENT = bigquery.Client()

    LOGGING_CLIENT.setup_logging()

QUAD_WORD = None
MODEL = None
SECRETS = None
PROJECT_ID = getenv("PROJECT_ID")


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
        return json.loads(Path("/secrets/app/secrets").read_text(encoding="utf-8"))

    #: Otherwise, try to load a local copy for local development
    secret_folder = Path(__file__).parent / "secrets"
    if secret_folder.exists():
        return json.loads((secret_folder / "secrets").read_text(encoding="utf-8"))

    raise FileNotFoundError("Secrets folder not found; secrets not loaded.")


def process_all_tiles(job_name, task_index, task_size, skip, take):
    """the code to run in the cloud run job that will run the full processing chain

    Args:
        job_name (str): the name of the run job. typically named after an animal in alphabetical order
        task_index (int): the index of the task running
        task_size (int): the number of index rows for a specific task to process
        skip (int): the number of index rows to skip (optional)
        take (int): the number of index rows to take (optional)

    Returns:
        None
    """
    task_start = perf_counter()

    #: calculate the number of rows to skip/take from the bigquery table
    #: if nonzero numbers are provided as environment variables, they will be used
    #: otherwise, we assume a static job_size environment variable is passed in and
    #: calculate skip/take based on the task_index
    if skip in (0, None) and take in (0, None):
        skip = task_index * task_size
        take = task_size

    logging.info("job name: %s task: %i getting rows from bigquery", job_name, task_index)
    rows = get_rows_from_gbq(skip, take)

    for row in rows:
        row_start = perf_counter()
        logging.info("starting work on col: %i row: %i", row.col_num, row.row_num)

        tiles = download_tiles(row.col_num, row.row_num, None)

        logging.info("download tiles finished in: %s", format_time(perf_counter() - row_start))

        mosaic_start = perf_counter()
        mosaic_image = build_mosaic_image(tiles, row.col_num, row.row_num, None)

        logging.info("mosaic finished in: %s", format_time(perf_counter() - mosaic_start))

        result_start = perf_counter()
        results = detect_towers(mosaic_image)

        logging.info("pytorch results finished in: %s", format_time(perf_counter() - result_start))

        if not results:
            logging.info("no image available")

            continue

        locate_start = perf_counter()
        results_df = locate_results(results, row.col_num, row.row_num)

        logging.info("locate results finished in: %s", format_time(perf_counter() - locate_start))

        if len(results_df.index) == 0:
            logging.info("no results to upload")

            continue

        logging.info(results_df.sort_values(by=["confidence"], ascending=True).head(20).to_string())
        logging.info("appending results for col: %i row: %i", row.col_num, row.row_num)

        append_start = perf_counter()
        append_status = append_results(results_df)

        logging.info("append results finished in: %s", format_time(perf_counter() - append_start))

        if append_status != "SUCCESS":
            logging.warning("append unsuccessful for col: %i row: %i, skipping index update", row.col_num, row.row_num)

            continue

        logging.info("updating index to 'processed' results for col: %i row: %i", row.col_num, row.row_num)

        index_start = perf_counter()
        update_index(row.col_num, row.row_num)

        logging.info("index update finished in: %s", format_time(perf_counter() - index_start))

        logging.info(
            "index col: %i row: %i processing finished in: %s",
            row.col_num,
            row.row_num,
            format_time(perf_counter() - row_start),
        )

    logging.info("task finished in: %s", format_time(perf_counter() - task_start))


def convert_to_cv2_image(image):
    """convert image (bytes) to a cv2 image object

    Args:
        image (bytes): The image (bytes) to convert

    Returns:
        cv2.Image: A cv2 image object
    """

    return cv2.imdecode(np.frombuffer(image, dtype=np.uint8), 1)  # 1 means flags=cv2.IMREAD_COLOR


def reorder_colors_to_rgb(image):
    """reorders np.ndarray image object from BGR to RGB

    Args:
        image (np.ndarray): The image to reorder colors

    Returns:
        np.ndarray: The image with reordered colors
    """

    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def get_rows_from_gbq(skip, take):
    """grab rows to process from bigquery indices table

    Args:
        skip (string): the number of leading rows to skip
        take (string): the number of rows to get form the table

    Returns:
        rows (iterator): big query row iterator
    """
    #: create sql query with skip/take for unprocessed rows
    #: order by row, col ascending to ensure consistent processing order
    sql = f"""
    SELECT * FROM `{PROJECT_ID}.indices.images_within_habitat`
    WHERE processed = false
    ORDER BY row_num, col_num
    LIMIT {take} OFFSET {skip}
    """

    #: perform query
    query_job = BIGQUERY_CLIENT.query(sql)
    rows = query_job.result()  #: waits for query to finish

    return rows


def _get_retry_session():
    """create a requests session that has a retry built into it

    Args:
        None

    Raises:
        error: The final error that causes worker_method to fail after 3 retries

    Returns:
        session: a new session
    """
    retries = 3
    backoff_factor = 0.3
    status_forcelist = (500, 502, 504)

    new_session = requests.Session()

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    new_session.mount("https://", adapter)

    return new_session


def get_tile(url):
    """Makes a requests.get call to the geocoding API.

    Meant to be called through a retry wrapper so that the RuntimeErrors get tried again a couple times before
        finally raising the error.

    Args:
        url (str): url for GET request

    Raises:
        RuntimeError: If the server does not return response and request.get returns a falsy object.
        RuntimeError: If the server returns a status code other than 200 or 404

    Returns:
        dict: The 'results' dictionary of the response json (location, score, and matchAddress)
    """

    session = _get_retry_session()

    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()  #: raise an exception if the status code is not 200 OK
    except requests.exceptions.Timeout:
        #: timeout occurred
        logging.debug("Timeout error occurred")

        return None

    except requests.exceptions.RequestException as error:
        #: other error occurred
        logging.debug("Error occurred: %s", error)

        return None

    #: the server times out and doesn't respond...is this needed??
    if response is None:
        logging.debug("GET call did not return a response")
        raise RuntimeError("No response from GET; request timeout?")

    #: the tile request is successful
    if response.status_code == 200:
        return response

    return None


def download_tiles(col, row, out_dir):
    """downloads image at specified col/row and each neighbor to the right, down, and right-down,
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

    base_url = f"https://discover.agrc.utah.gov/login/path/{SECRETS.QUAD_WORD}/tiles/utah/20"
    col_num = int(col)
    row_num = int(row)

    urls = []
    #: build url for primary tile (top-left)
    urls.append(f"{base_url}/{col_num}/{row_num}")
    #: build url for top-right tile
    urls.append(f"{base_url}/{col_num + 1}/{row_num}")
    #: build url for bottom-left tile
    urls.append(f"{base_url}/{col_num}/{row_num + 1}")
    #: build url for bottom-right tile
    urls.append(f"{base_url}/{col_num + 1}/{row_num + 1}")

    #: make requests for each url/tile in the url list
    tile_list = []
    for url in urls:
        tile = get_tile(url)

        if tile is None:
            continue

        tile_list.append(tile.content)

    if not all(tile_list):
        logging.debug("at least one tile failed to download; aborting...")

        return None

    logging.debug("download function is working with %s", type(tile_list[0]))

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

        return None

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

    logging.debug("mosaic is starting with %s", type(tiles[0]))

    i = 0
    for tile in tiles:
        #: convert from bytes to cv2
        img = convert_to_cv2_image(tile)
        #: add image into the mosaic
        row_start = (math.floor(i / number_columns)) * tile_width
        col_start = (i % number_columns) * tile_width
        mosaic_image[row_start : row_start + tile_width, col_start : col_start + tile_width] = img

        i += 1

    logging.debug("mosaic is returning %s", type(mosaic_image))

    if out_dir:
        if not out_dir.exists():
            out_dir.mkdir(parents=True)

        mosaic_outfile = out_dir / f"{tile_name}_mosaic.jpg"
        logging.debug("saving to %s", mosaic_outfile)
        cv2.imwrite(str(mosaic_outfile), mosaic_image)

        return mosaic_image

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

    if not model_weight_path.is_file():
        logging.error("the model weights file does not exist: %s", model_weight_path)

        raise FileNotFoundError("the model weights file does not exist")

    if not yolov5_path.is_dir():
        logging.error("the yolov5 directory does not exist, was it cloned? %s", yolov5_path)

        raise FileNotFoundError("the yolov5 directory does not exist")

    try:
        model = torch.hub.load(str(yolov5_path), "custom", path=str(model_weight_path), source="local")
    except Exception as ex:
        logging.error("the tower scout yolov5 model failed to load: %s", ex)

        raise ex

    return model


def _get_model():
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
    if image is None:
        logging.info("no image to detect towers on: %s", type(image))
        return None

    towerscout_model = _get_model()

    #: adjust model confidence threshold for accepting a detection
    #: model.conf - range of values is 0 to 1
    #: lower values mean that more detections are allowed into the results
    #: default value is 0.25, but we've noticed it missing some cooling towers
    #: 0.005 gets more, but 0.007 seems to be a decent distinguishing value
    #: we want to detect more than necessary, we can always weed out bad ones with a query later
    logging.debug("initial model confidence threshold: %s", towerscout_model.conf)
    towerscout_model.conf = 0.007
    logging.info("adjusted model confidence threshold: %s", towerscout_model.conf)

    #: adjust model overlap threshold for accepting a detection (higher means more detections)
    #: model.iou - range of values is 0 to 1
    #: higher values mean greater overlap is allowed (more detections)
    #: lower values mean more spacing is required between detections (fewer detections)
    #: we want lower, so the same tower isn't detected multiple times
    logging.debug("initial model confidence threshold: %s", towerscout_model.iou)
    towerscout_model.iou = 0.25
    logging.debug("adjusted model confidence threshold: %s", towerscout_model.iou)

    logging.info("detect is working with %s", type(image))

    if isinstance(image, np.ndarray):
        logging.info("reordering colors to RGB")
        image = reorder_colors_to_rgb(image)

    scan_start = perf_counter()
    results = towerscout_model(image)
    logging.info("time to scan image: %s", format_time(perf_counter() - scan_start))

    return results


def locate_results(results, col, row):
    """locate detection results and calculate coordinates

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
    try:
        tile = mercantile.ul(int(col), int(row), zoom_level)
    except ValueError as error:
        logging.error("error getting tile coordinates on %s, %s: %s", col, row, error, exc_info=True)

        return results_df

    #: calculate centroid in pixels
    results_df["x_centroid_px"] = (results_df["xmin"] + results_df["xmax"]) / 2
    results_df["y_centroid_px"] = (results_df["ymin"] + results_df["ymax"]) / 2

    #: project tile coords to web mercator (3857)
    wgs84 = 4326
    web_mercator = 3857

    transformer = pyproj.Transformer.from_crs(
        pyproj.CRS.from_epsg(wgs84), pyproj.CRS.from_epsg(web_mercator), always_xy=True
    )
    x, y = transformer.transform(tile.lng, tile.lat)

    #: calculate centroid x/y coords in web mercator
    meters_per_pixel = 0.1492910708688
    results_df["x_centroid_3857"] = x + results_df["x_centroid_px"] * meters_per_pixel
    results_df["y_centroid_3857"] = y - results_df["y_centroid_px"] * meters_per_pixel

    return results_df


def append_results(results_df):
    """append results dataframe into bigquery results table

    Args:
        results_df (dataframe): dataframe with cooling tower detection results

    Returns:
        None
    """
    table_id = f"{PROJECT_ID}.output_data.cooling_tower_results"

    #: specify the type of columns whose type cannot be auto-detected. For
    #: the "name" column uses pandas dtype "object", so it is ambiguous.
    job_config = bigquery.LoadJobConfig(
        schema=[bigquery.SchemaField("name", bigquery.enums.SqlTypeNames.STRING)],
        write_disposition="WRITE_APPEND",
        create_disposition="CREATE_NEVER",
    )

    job = BIGQUERY_CLIENT.load_table_from_dataframe(results_df, table_id, job_config=job_config, location="US")

    try:
        job_result = job.result()  # Waits for table load to complete.
    except Exception as ex:
        logging.error("unable to append rows into the results table! %s", ex)

        if job.errors is not None:
            logging.error("encountered the following errors:")

            for error in job.errors:
                logging.error(error)

        return

    logging.info("insert result: %s", job_result)

    #: return a fresh job status
    if job is None:
        return None

    if job.job_id is None:
        return None

    status = BIGQUERY_CLIENT.get_job(job.job_id).state

    return status


def update_index(col, row):
    """update the `images_within_habitat` table in bigquery after a row is processed

    Args:
        col (str): the column of the WMTS index for the tile of interest (top-left tile)
        row (str): the row of the WMTS index for the tile of interest (top-left tile)

    Returns:
        None
    """
    table_id = f"{PROJECT_ID}.indices.images_within_habitat"

    #: create dml statement to update specific row
    dml = f"""
    UPDATE `{table_id}`
    SET processed = true
    WHERE col_num = {col} AND row_num = {row}
    """

    query = BIGQUERY_CLIENT.query(dml)

    try:
        query_result = query.result()  # Waits for update to complete.
    except Exception as ex:
        logging.error("unable to update index on col: %i, row: %i, %s", col, row, ex)

        return

    if query_result.total_rows == 0:
        logging.warning("no rows were updated in the index table!")

    logging.info("rows updated in the index table: %i", query_result.total_rows)


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
