FROM python:3.8-slim
WORKDIR /app
COPY . .
COPY requirements.txt /app
RUN python3 -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt --no-cache-dir
CMD ["/bin/bash", "./start_backend.sh"]