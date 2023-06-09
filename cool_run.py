#!/usr/bin/env python
# * coding: utf8 *
"""
the file to run to start the project
"""

import logging
from os import getenv
from time import perf_counter

import cool

#: Set up variables
JOB_NAME = getenv("JOB_NAME")
TASK_INDEX = int(getenv("CLOUD_RUN_TASK_INDEX") or 0)
TASK_SIZE = int(getenv("JOB_SIZE") or 0)
SKIP = int(getenv("SKIP") or 0)
TAKE = int(getenv("TAKE") or 0)


def process_all_tiles():
    """the main function to execute when cloud run starts the cooling tower detection job"""

    job_start = perf_counter()

    cool.process_all_tiles(JOB_NAME, TASK_INDEX, TASK_SIZE, SKIP, TAKE)

    logging.info(
        "job name: %s finished entire job in: %s",
        JOB_NAME,
        cool.format_time(perf_counter() - job_start),
    )


if __name__ == "__main__":
    process_all_tiles()
