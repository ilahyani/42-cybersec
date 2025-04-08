FROM python:3.9-slim

WORKDIR /app

RUN pip install "fastapi[standard]" psycopg2-binary

CMD ["fastapi", "run", "/app/vulnerable_postgresql_db.py", "--host", "0.0.0.0", "--port", "8001"]
