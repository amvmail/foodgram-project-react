#!/bin/bash
# python3 manage.py makemigrations --noinput && \
python3 manage.py migrate --fake recipes --noinput && \
python3 manage.py collectstatic --noinput && \
python3 manage.py load_data && \
gunicorn foodgram.wsgi:application --bind 0:8000