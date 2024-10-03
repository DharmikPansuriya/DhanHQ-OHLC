FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
LABEL maintainer="Dharmik Pansuriya <service.dharmikpansuriya@gmail.com>"

WORKDIR /app/

RUN apt-get install libpq-dev

RUN apt-get update && apt-get install -y wkhtmltopdf
COPY ./requirements/ /app/requirements/
RUN pip install --no-cache-dir --upgrade -r /app/requirements/production.txt

COPY . /app
ENV PYTHONPATH=/app
