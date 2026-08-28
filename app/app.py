import logging
import os
import socket

from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

metrics = PrometheusMetrics(app)

INSTANCE_NAME = os.getenv(
    "INSTANCE_NAME",
    socket.gethostname()
)


@app.route("/")
def index():
    app.logger.info(
        "Solicitud atendida por %s",
        INSTANCE_NAME
    )

    return jsonify({
        "status": "OK",
        "message": "Proyecto DevSecOps funcionando",
        "instance": INSTANCE_NAME
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "instance": INSTANCE_NAME
    })


@app.route("/error")
def generate_error():
    app.logger.error(
        "Error de prueba generado en %s",
        INSTANCE_NAME
    )

    return jsonify({
        "status": "ERROR",
        "instance": INSTANCE_NAME
    }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )

