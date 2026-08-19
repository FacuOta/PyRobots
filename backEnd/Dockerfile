# Imagen del backend, pensada para Hugging Face Spaces (SDK docker).
#
# Dos cosas mandan acá:
#  - Spaces sirve el contenedor por el puerto 7860.
#  - El sistema de archivos es de solo lectura salvo /tmp, así que la base y los
#    archivos subidos van ahí. Se pierden en cada reinicio: es una demo.

FROM python:3.11-slim

# gcc hace falta para compilar algunas ruedas (bcrypt) en slim.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y gcc libc6-dev && apt-get autoremove -y

COPY src/ ./src/
COPY Robot/ ./Robot/

# Los import del proyecto son planos (from crud_handlers import *), así que la
# app tiene que correr parada dentro de src/.
WORKDIR /app/src

ENV PYROBOTS_DATA=/tmp/pyrobots \
    PYTHONUNBUFFERED=1

EXPOSE 7860

CMD ["uvicorn", "endpoints:app", "--host", "0.0.0.0", "--port", "7860"]
