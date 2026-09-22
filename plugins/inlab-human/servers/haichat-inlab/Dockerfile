# ── build the console SPA ────────────────────────────────────────────────────
FROM node:20-slim AS web
WORKDIR /web
COPY web/package.json web/package-lock.json* ./
RUN npm install
COPY web/ ./
RUN npm run build

# ── serve it, plus the prediction REST API ───────────────────────────────────
FROM python:3.11-slim
WORKDIR /app

COPY pyproject.toml .
COPY main.py console_api.py ./
RUN pip install --no-cache-dir .

COPY --from=web /web/dist ./web/dist

# The prediction engine and the cohort are MOUNTED, never baked in:
#   /engine  = Tools/plugins/inlab-human/mcp-servers/endpoint-predict  (shared code)
#   the stores = study-specific data, which must never live in this image.
ENV INLAB_ENGINE=/engine

EXPOSE 8091
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8091"]
