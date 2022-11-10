FROM python:3.10.8

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN pip install --upgrade pip

RUN pip install uwsgi
RUN pip install paddleocr --upgrade
RUN pip install paddlepaddle

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY base base/
COPY vng vng/
COPY manage.py .

ENV DJANGO_SETTINGS_MODULE=vng.settings
ARG DJANGO_SECRET_KEY=insecure_docker_build_key
RUN SECRET_KEY=$DJANGO_SECRET_KEY python manage.py collectstatic --no-input

EXPOSE 8000
CMD uwsgi
