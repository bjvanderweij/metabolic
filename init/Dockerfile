FROM python:3.8.3-buster

RUN pip install --upgrade pip

COPY  requirements.txt . 
RUN pip install -r requirements.txt

COPY ./src /app
WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/mblib/src"
