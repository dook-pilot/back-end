# pull official base image
FROM python:3.10.8

# ENV PYTHONUNBUFFERED 1

RUN adduser docker;echo 'docker:123' | chpasswd
USER 0
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PATH="/home/docker/.local/bin:${PATH}"
RUN pip install --upgrade pip
RUN pip install common dual tight data prox
RUN pip install paddlepaddle --timeout=200
COPY ./requirements.txt .
RUN yes | pip install -r requirements.txt --timeout=1800

RUN apt-get -y update && apt-get -y install libgl1
RUN apt-get install -y libgdal-dev g++ --no-install-recommends && \
    apt-get clean -y
    
RUN apt-get install -y nginx
    
# ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
# ENV C_INCLUDE_PATH=/usr/include/gdal

COPY . .
# COPY base base/
# COPY vng vng/
# COPY manage.py .

# ENV DJANGO_SETTINGS_MODULE=vng.settings
# ARG DJANGO_SECRET_KEY=insecure_docker_build_key
# RUN SECRET_KEY=$DJANGO_SECRET_KEY python manage.py collectstatic --no-input

# EXPOSE 8000
# CMD uwsgi