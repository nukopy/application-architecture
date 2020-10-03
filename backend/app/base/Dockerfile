FROM python:3.8-slim

LABEL  maintainer "nukopy <pytwbf201830@gmail.com>"

WORKDIR /app

# install packages
RUN set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install -U --no-cache-dir poetry \
    && rm -rf /var/lib/apt/lists/*

# install Python packages
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install

# add source code
COPY ./ ./
