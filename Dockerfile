# Image de production de Là-haut : le site FastAPI, servi par uvicorn.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # Les catalogues CelesTrak se gardent dans /tmp : le disque de l'offre gratuite est éphémère.
    LA_HAUT_CACHE=/tmp/la-haut/visual.tle \
    # L'hébergeur fournit le port dans $PORT ; 8000 en local.
    PORT=8000

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install .

RUN useradd --create-home --uid 10001 la-haut
USER la-haut

EXPOSE 8000

CMD ["sh", "-c", "exec uvicorn --factory la_haut.composition:build_web_app --host 0.0.0.0 --port \"$PORT\""]
