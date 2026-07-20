"""Flask To-Do app — Git workflow assignment."""
import json
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MongoDB (Atlas). Set MONGO_URI in .env — the client connects lazily.
MONGO_URI = os.getenv("MONGO_URI")
_mongo = MongoClient(MONGO_URI) if MONGO_URI else None
todos = _mongo["todo_db"]["todos"] if _mongo is not None else None


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


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    """Accept itemName + itemDescription (form or JSON) via POST and store in MongoDB."""
    data = request.form if request.form else (request.get_json(silent=True) or {})
    item_name = data.get("itemName")
    item_description = data.get("itemDescription", "")
    if not item_name:
        return jsonify({"error": "itemName is required"}), 400

    doc = {"itemName": item_name, "itemDescription": item_description}
    if todos is not None:
        result = todos.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
    else:
        return jsonify({"error": "MONGO_URI not configured"}), 500
    return jsonify({"status": "saved", "item": doc}), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)
