FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install --upgrade pip

COPY  requirements.txt . 
RUN pip install -r requirements.txt

COPY ./src /app
WORKDIR /app
