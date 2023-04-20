#!/usr/bin/env python
# * coding: utf8 *
"""
DHHS Cooling Tower object detection

Usage:
    cool_cli.py download-tiles <col> <row> [--save-to=location --mosaic]
    cool_cli.py detect-towers <file_name> [(--locate-results <col> <row>)] 
    cool_cli.py process-tiles <col> <row> [--save-to=location]
    cool_cli.py process-upload <skip> <take>

Options:
    --from=location                 The bucket or directory to operate on
    --task-index=index              The index of the task running
    --instances=size                The number of containers running the job [default: 10]
    --save-to=location              The location to output the stuff
Examples:
    python cool_cli.py download-tiles 198259 394029 --save-to=./tiles
    python cool_cli.py download-tiles 198259 394029 --save-to=./mosaics --mosaic
    python cool_cli.py detect-towers ./mosaics/198263_394029_mosaic.jpg
    python cool_cli.py detect-towers ./mosaics/198263_394029_mosaic.jpg --locate-results 198263 394029
    python cool_cli.py process-tiles 198263 394029 --save-to=./results
    python cool_cli.py process-upload 10 20


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

    if args["download-tiles"]:
        output_directory = None

        print("downloading tiles ...")
        if args["--save-to"]:
            output_directory = Path(args["--save-to"])

        col, row = args["<col>"], args["<row>"]
        tiles = cool.download_tiles(col, row, output_directory)

        if args["--mosaic"]:
            print("building mosaic ...")

            mosaic_image = cool.build_mosaic_image(tiles, col, row, output_directory)

        return

    if args["detect-towers"]:
        image = Path(args["<file_name>"])
        results = cool.detect_towers(image)

        if not results:
            print("no image available")

            return

        results.print()

        if args["--locate-results"]:
            col, row = args["<col>"], args["<row>"]
            results_df = cool.locate_results(results, col, row)

            print(results_df.head().to_string())

        return

    if args["process-tiles"]:
        output_directory = None

        print("downloading tiles ...")
        col, row = args["<col>"], args["<row>"]
        tiles = cool.download_tiles(col, row, output_directory)

        if args["--save-to"]:
            output_directory = Path(args["--save-to"])

        mosaic_image = cool.build_mosaic_image(tiles, col, row, output_directory)

        results = cool.detect_towers(mosaic_image)

        if not results:
            print("no image available")

            return

        results.print()

        results_df = cool.locate_results(results, col, row)

        print(results_df.sort_values(by=['confidence'], ascending=True).head(20).to_string())

        return


    if args["process-upload"]:
        output_directory = None

        rows = cool.get_rows_from_gbq(args["<skip>"], args["<take>"])

        for row in rows:
            print("downloading tiles ...")
            tiles = cool.download_tiles(row.col_num, row.row_num, output_directory)

            mosaic_image = cool.build_mosaic_image(tiles, row.col_num, row.row_num, output_directory)

            results = cool.detect_towers(mosaic_image)

            if not results:
                print("no image available")

                continue

            results.print()

            results_df = cool.locate_results(results, row.col_num, row.row_num)

            if len(results_df.index) == 0:
                print('no results to upload')

                continue

            cool.append_results(results_df)
            print('appended results for col: {row.col_num} row: {row.row_num} ')

            print(results_df.sort_values(by=['confidence'], ascending=True).head(20).to_string())
        
        return

if __name__ == "__main__":
    main()
