FROM python:3.9-slim

WORKDIR /app

RUN pip install "fastapi[standard]" mysql-connector-python

CMD ["fastapi", "run", "/app/vulnerable_mysql_db.py", "--host", "0.0.0.0", "--port", "8000"]
