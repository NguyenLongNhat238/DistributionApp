# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install GNU gettext tools
RUN apt-get update && \
    apt-get install -y gettext

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /distributions

COPY requirements.txt /distributions/
RUN pip install -r requirements.txt
COPY . /distributions/

