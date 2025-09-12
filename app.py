from flask import Flask, jsonify, Response, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)


REQUEST_COUNT = Counter('flask_requests_total', 'Total HTTP requests (flask)')

@app.before_request
def before_request():

    REQUEST_COUNT.inc()

@app.route("/")
def index():
    return jsonify(message="Hello from Flask app!")

@app.route("/health")
def health():
    return jsonify(status="UP", message="Application is healthy!")

@app.route("/metrics")
def metrics():
    # Prometheus metrics endpoint
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
