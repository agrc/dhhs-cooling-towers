# dhhs-cooling-towers

Tools to extract cooling tower locations from aerial imagery

## Prerequisites
1. Create WMTS index
   - Run `prerequisites\polars_build_offet_index.py`
   - This creates a parquet file (`imagery_index.parquet`) that will be loaded into BigQuery by terraform
1. Create the processing footprint
   - This was done manually in ArcGIS Pro with the following steps:
      1. Buffer [Utah Census Places 2020](https://opendata.gis.utah.gov/datasets/utah-census-places-2020/explore) by 800m
      1. Query [Utah Buildings](https://opendata.gis.utah.gov/datasets/utah-buildings/explore) down to those larger than 464.5 sq m (5000 sq ft)
      1. Select by Location the queried buildings that are more than 800m from the census places buffer
      1. Export selected buildings to a new layer
      1. Buffer the new buildings layer by 800m
      1. Combine the buffered census places and buffered buildings into a single polygon layer
      1. Simplify the combined polygon layer to remove vertices
      1. Project the simplified polygon layer to WGS84 (EPSG: 4326)
      1. Export the projected polygon layer to shapefile (processing_footprint.shp)
      1. Convert the processing footprint from shapefile to CSV with geometries represented as GeoJSON using GDAL
         - Use the process outlined in this [Blog Post](https://medium.com/google-cloud/how-to-load-geographic-data-like-zipcode-boundaries-into-bigquery-25e4be4391c8) about loading geographic data into BigQuery
         - `ogr2ogr -f csv -dialect sqlite -sql "select AsGeoJSON(geometry) AS geom, * from processing_footprint" footprints_in_4326.csv processing_footprint.shp`
      1. The `footprints_in_4326.csv` file will be loaded into BigQuery by terraform



## Data preparation

1. Run the tower scout terraform
   - this is a private github repository
1. Execute the two data transfers in order
1. Execute the two scheduled queries in order
1. Export `{PROJECT_ID}.indices.images_within_habitat` to GCS

   _there is a terraform item for this but I don't know how it will work since the data transfers are manual and the table may not exist_

   - GCS Location: `{PROJECT_ID}.images_within_habitat.csv`
   - Export format: `CVS`
   - Compression: `None`

1. Using the cloud sql proxy

   1. Create a cloud sql table for the task tracking

      ```sql
      CREATE TABLE public.images_within_habitat (
         row_num int NULL,
         col_num int NULL,
         processed bool NULL DEFAULT false
      );

      CREATE UNIQUE INDEX idx_images_within_habitat_all ON public.images_within_habitat USING btree (row_num, col_num, processed);
      ```

      1. Create a cloud sql table for the results

      ```sql
      CREATE TABLE public.cooling_tower_results (
         envelope_x_min decimal NULL,
         envelope_y_min decimal NULL,
         envelope_x_max decimal NULL,
         envelope_y_max decimal NULL,
         confidence decimal NULL,
         object_class int NULL,
         object_name varchar NULL,
         centroid_x_px decimal NULL,
         centroid_y_px decimal NULL,
         centroid_x_3857 decimal NULL,
         centroid_y_3857 decimal NULL
      );
      ```

      1. Grant access to users

      ```sql
         GRANT pg_read_all_data TO "cloud-run-sa@ut-dts-agrc-dhhs-towers-dev.iam";
         GRANT pg_write_all_data TO "cloud-run-sa@ut-dts-agrc-dhhs-towers-dev.iam";
      ```

1. Import the CSV into the `images_within_habitat` table

## To work with the CLI locally

1. Download the PyTorch model weights file and place in the `tower_scout` directory
   - Add URL
1. Clone YOLOv5 repository from parent directory

   ```sh
   git clone https://github.com/ultralytics/yolov5
   ```

1. Create virtual environment from the parent directory with Python 3.10

   ```sh
   python -m venv .env
   .env\Scripts\activate.bat
   pip install -r requirements.dev.txt
   ```

## CLI

To work with the CLI,

1. Create a python environment and install the `requirements.dev.txt` into that environment
1. Execute the CLI to see the commands and options available
   - `python cool_cli.py`

## Testing

## Cloud Run Job

To test a small amount of data

1. Set the number of tasks to 1
1. Set the environment variables
   - `SKIP`: int e.g. 1106600
   - `TAKE`: int e.g. 50
   - `JOB_NAME`: string e.g. alligator

To run a batch job

1. Set the number of tasks to your desired value e.g. 10000
1. Set the concurrency to your desired value e.g. 35
1. Set the environment variables
   - `JOB_NAME`: string e.g. alligator
   - `JOB_SIZE`: int e.g. 50 (this value needs to be processable within the timeout)

Our metrics show that we can process 10 jobs a minute. The default cloud run timeout is 10 minutes.

## References for Identifying Cooling Towers in Aerial Imagery
- [CDC Procedures for Identifying Cooling Towers](https://www.cdc.gov/legionella/health-depts/environmental-inv-resources/id-cooling-towers.html)
- [CDC Photos of Cooling Towers](https://www.cdc.gov/legionella/health-depts/environmental-inv-resources/cooling-tower-images.html)
- [California Department of Public Health: Cooling Tower Identification 101](https://www.cdph.ca.gov/Programs/CID/DCDC/CDPH%20Document%20Library/CoolingTowerIDGuideProtocol.pdf)
- [California Department of Public Health: Cooling Tower Identification Guide Supplement](https://www.cdph.ca.gov/Programs/CID/DCDC/CDPH%20Document%20Library/CTIDGuideSupplement.pdf)
