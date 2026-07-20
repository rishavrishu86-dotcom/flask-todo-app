"""Flask To-Do app — Git workflow assignment."""
import json
import os

from flask import Flask, jsonify, render_template

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_data():
    """Read the JSON file that backs the /api route."""
    with open(os.path.join(BASE_DIR, "data.json")) as f:
        return json.load(f)


@app.route("/")
def home():
    """Home / To-Do page."""
    return render_template("index.html")


@app.route("/api")
def api():
    """Return the contents of data.json as JSON."""
    return jsonify(load_data())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
