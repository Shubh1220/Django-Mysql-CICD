# ---- Base image ----------------------------------------------------------
FROM python:3.11-slim

WORKDIR /app

# ---- System deps needed to build mysqlclient ------------------------------
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ---- Python deps ----------------------------------------------------------
COPY requirements.txt .
RUN pip install mysqlclient
RUN pip install --no-cache-dir -r requirements.txt

# ---- App code ---------------------------------------------------------
COPY . .

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
