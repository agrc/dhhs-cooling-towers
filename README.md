# dhhs-cooling-towers

Tools to extract cooling tower locations from aerial imagery

## To work with the CLI locally

1. Download the PyTorch model weights file and place in the `tower_scout` directory
   - Add URL
1. Clone YOLOv5 repository from parent directory

   ```sh
   git clone https://github.com/ultralytics/yolov5
   ```

1. Create virtual environment from parent directory with Python 3.10

   ```sh
   python -m venv .env
   .env\Scripts\activate.bat
   pip install -r requirements.dev.txt
   cd yolov5
   pip install -r requirements.txt
   ```

## CLI

To work with the CLI,

1. Create a python environment and install the `requirements.dev.txt` into that environment
1. Execute the CLI to see the commands and options available
   - `python cool_cli.py`

## Testing

## Cloud Run Job

To test a small amount of data with a coud run job

1. Set the number of tasks to 1
1. Set environment variables
   - `SKIP`: int e.g. 1106600
   - `TAKE`: int e.g. 50
   - `JOB_NAME`: string e.g. alligator
