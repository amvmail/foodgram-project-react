FROM python:3.7-slim

WORKDIR /app

COPY . .

COPY requirements.txt /app

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r /app/requirements.txt --no-cache-dir

CMD ["/bin/bash", "./start.sh"]

# CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
