FROM python:3.12-slim

WORKDIR /backend

RUN apt-get update && apt-get install -y \
  gcc \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install --upgrade pip \
  && pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "./scripts/wait-for-db.sh db alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
