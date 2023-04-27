#!/usr/bin/env python
# * coding: utf8 *
"""
the file to run to start the project
"""

import logging
from os import getenv
from sys import stdout
from time import perf_counter

import cool

#: Set up logging
logging.basicConfig(
    stream=stdout,
    format="%(levelname)-7s %(asctime)s %(module)10s:%(lineno)5s %(message)s",
    datefmt="%m-%d %H:%M:%S",
    level=logging.INFO,
)

#: Set up variables
JOB_NAME = getenv("JOB_NAME")
TASK_INDEX = int(getenv("CLOUD_RUN_TASK_INDEX") or 0)


def mosaic_all_circles():
    """the main function to execute when cloud run starts the circle detection job"""

    job_start = perf_counter()

    cool.mosaic_all_circles(JOB_NAME, BUCKET_NAME, OUTPUT_BUCKET_NAME, INDEX, TASK_INDEX, TASK_COUNT, TOTAL_FILES)

    logging.info(
        "job name: %s task %i: entire job %s",
        JOB_NAME,
        TASK_INDEX,
        cool.format_time(perf_counter() - job_start),
    )


if __name__ == "__main__":
    run()
