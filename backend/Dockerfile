FROM python:3.9-alpine

ENV LANG C.UTF-8
ENV TZ Asia/TOKYO

RUN apk add --update --no-cache make bash gcc g++ tzdata git\
  && pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED 1
WORKDIR /var/www/html

COPY requirements.txt .


ADD wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh