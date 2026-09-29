import os
import time
import random

from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST


app = Flask(__name__)
app.json.ensure_ascii = False


REQUEST_COUNT = Counter(
    "app_http_requests_total",
    "Total de requisições HTTP",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "app_http_request_duration_seconds",
    "Tempo de resposta das requisições HTTP",
    ["endpoint"]
)


@app.route("/")
def home():
    start_time = time.time()

    response = {
        "message": "Olá teste Observability!",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "development")
    }

    REQUEST_COUNT.labels(
        method="GET",
        endpoint="/",
        status="200"
    ).inc()

    REQUEST_LATENCY.labels(
        endpoint="/"
    ).observe(time.time() - start_time)

    return jsonify(response), 200


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/ready")
def ready():
    return jsonify({
        "status": "ready"
    }), 200


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


@app.route("/work")
def work():
    start_time = time.time()

    # Simula algum processamento
    time.sleep(random.uniform(0.05, 0.3))

    REQUEST_COUNT.labels(
        method="GET",
        endpoint="/work",
        status="200"
    ).inc()

    REQUEST_LATENCY.labels(
        endpoint="/work"
    ).observe(time.time() - start_time)

    return jsonify({
        "message": "Work completed"
    }), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080"))
    )