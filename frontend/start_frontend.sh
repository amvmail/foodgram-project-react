#!/bin/bash
cp -r build result_build && \
python3 manage.py collectstatic --noinput