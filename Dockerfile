FROM python:3.12.3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Upgrade pip, setuptools, and importlib-metadata
RUN pip install --upgrade pip setuptools importlib-metadata

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .