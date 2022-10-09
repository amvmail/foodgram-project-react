#!/bin/bash
python3 manage.py migrate --noinput && \
python3 manage.py collectstatic --noinput && \
gunicorn foodgram.wsgi:application --bind 0:8000