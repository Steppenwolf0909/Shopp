FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /web
WORKDIR /web
COPY requirements.txt /web/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /web/






