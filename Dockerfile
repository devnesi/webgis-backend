FROM python:3.7
ENV LANG C.UTF-8

RUN mkdir /django

ADD requirements.txt /django/requirements.txt
RUN pip install -r /django/requirements.txt

RUN apt-get -y update && apt-get -y autoremove && apt-get install binutils libproj-dev gdal-bin -y

COPY . /django
WORKDIR /django

EXPOSE 8000

CMD gunicorn -b 0.0.0.0:8000 --workers 15 --timeout 300 --log-level=debug --log-file /tmp/log webgis.wsgi
