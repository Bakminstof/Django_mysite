FROM python:3.10-alpine

WORKDIR /usr/src/mysite

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY mysite ./

CMD gunicorn mysite.wsgi:application --bind $GUNICORN_HOST:$GUNICORN_PORT
