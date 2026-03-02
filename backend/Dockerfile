FROM python:3.12-slim

WORKDIR /backend

RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  libpq-dev \
  netcat-openbsd \
  && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen

ENV PATH="/backend/.venv/bin:$PATH"

COPY . .

EXPOSE 8000

ENTRYPOINT ["./scripts/entrypoint.sh"]