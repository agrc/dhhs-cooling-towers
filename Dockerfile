FROM python:3.10-slim

USER root

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN useradd -s /bin/bash dummy

WORKDIR /app

COPY tower_scout/* tower_scout/
COPY yolov5/ yolov5/

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 cache purge

COPY cool.py cool.py
COPY cool_run.py cool_run.py

USER dummy
ENTRYPOINT ["python3", "cool_run.py"]
