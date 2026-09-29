FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app
COPY main.py /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["flask","--app","main","run","--host","0.0.0.0","--port","8080"]

