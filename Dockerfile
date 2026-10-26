# Image de production de Là-haut : le site FastAPI, servi par uvicorn.

# La page, construite par Vite ; l'image finale n'en garde que les fichiers construits.
FROM node:24-slim AS front
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend ./
RUN npm run build

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # Les catalogues CelesTrak se gardent dans /tmp : le disque de l'offre gratuite est éphémère.
    LA_HAUT_CACHE=/tmp/la-haut/visual.csv \
    # L'hébergeur fournit le port dans $PORT ; 8000 en local.
    PORT=8000

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY --from=front /app/src/la_haut/interface/http/static ./src/la_haut/interface/http/static
RUN pip install .

RUN useradd --create-home --uid 10001 la-haut
USER la-haut

EXPOSE 8000

CMD ["sh", "-c", "exec uvicorn --factory la_haut.composition:build_web_app --host 0.0.0.0 --port \"$PORT\""]
