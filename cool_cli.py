#!/usr/bin/env python
# * coding: utf8 *
"""
DHHS Cooling Tower object detection

Usage:
    cool_cli.py download tiles <col> <row> [--save-to=location] (--mosaic --detect --parse-results)
    cool_cli.py detect towers <file_name>

Options:
    --from=location                 The bucket or directory to operate on
    --task-index=index              The index of the task running
    --instances=size                The number of containers running the job [default: 10]
    --save-to=location              The location to output the stuff
Examples:
    python cool_cli.py download tiles 198259 394029 --save-to=./data --mosaic
    python cool_cli.py download tiles 198402 394067 --mosaic --detect
    python cool_cli.py download tiles 198402 394067 --mosaic --detect --parse-results
    python cool_cli.py detect towers ./data/198259_394029.jpg

"""

import logging
from pathlib import Path
from sys import stdout

from docopt import docopt

import cool

logging.basicConfig(
    stream=stdout,
    format="%(levelname)-7s %(asctime)s %(module)10s:%(lineno)5s %(message)s",
    datefmt="%m-%d %H:%M:%S",
    level=logging.INFO,
)


def main():
    """doc string"""
    args = docopt(__doc__, version="1.0")  # type: ignore

    if args["download"] and args["tiles"]:
        output_directory = None

        print('downloading tiles ...')
        col, row = args["<col>"], args["<row>"]
        tiles = cool.download_tiles(col, row)

        if args["--mosaic"]:
            if args["--save-to"]:
                output_directory = Path(args["--save-to"])
            
            mosaic_image = cool.build_mosaic_image(tiles, col, row, output_directory)

        if args["--detect"]:
            results = cool.detect_towers(mosaic_image)

            results.print()

        if args["--parse-results"]:
            results = cool.parse_results(results, col, row)

        return

    if args["detect"] and args["towers"]:
        image = Path(args["<file_name>"])
        results = cool.detect_towers(image)

        results.print()

        return


if __name__ == "__main__":
    main()
