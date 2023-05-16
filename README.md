# dhhs-cooling-towers

Tools to extract cooling tower locations from aerial imagery

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
