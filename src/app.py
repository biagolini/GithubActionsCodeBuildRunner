import platform

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/arch")
def arch():
    """Return the CPU architecture the container runs on (x86_64 or aarch64)."""
    return jsonify(architecture=platform.machine())


@app.get("/add/<int(signed=True):a>/<int(signed=True):b>")
def add(a, b):
    return jsonify(operation="add", a=a, b=b, result=a + b)


@app.get("/subtract/<int(signed=True):a>/<int(signed=True):b>")
def subtract(a, b):
    return jsonify(operation="subtract", a=a, b=b, result=a - b)


@app.get("/multiply/<int(signed=True):a>/<int(signed=True):b>")
def multiply(a, b):
    return jsonify(operation="multiply", a=a, b=b, result=a * b)


@app.get("/divide/<int(signed=True):a>/<int(signed=True):b>")
def divide(a, b):
    if b == 0:
        return jsonify(error="division by zero"), 400
    return jsonify(operation="divide", a=a, b=b, result=a / b)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
