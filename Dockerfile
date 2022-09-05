FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./requirements.txt /requirements.txt

RUN python3 -m pip install -r /requirements.txt

COPY ./app /app
