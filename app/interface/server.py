"""
@author Aaditya and Sam Blesswin
@version 0.1
@since 17-03-2024
This file maps the learned bloom filter APIs to REST API endpoints.
USE IN REST MODE ONLY
"""

from flask import Flask, request, jsonify
from api import LearnedBloomFilter, MODE
from Attacker import attacker
from Stream import Producer

app = Flask(__name__)


@app.route("/")
def base():
    return


@app.route("/insert", methods=["POST"])
def insert():
    data = request.get_json()
    lbf.insert(int(data["key"]))
    return "", 201


@app.route("/query/<key>")
def query(key):
    found = False
    result = lbf.query(int(key))
    return result, 200


@app.route("/produce")
def produce():
    try:
        Producer.run()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "All data has been sent to the Kafka topic.",
                }
            ),
            200,
        )
    except Exception as e:
        return (jsonify({"status": "error", "message": str(e)}), 500)


@app.route("/consume")
def consume():
    success, message = lbf.consume()
    if success:
        return jsonify({"status": "success", "message": message}), 200
    else:
        return jsonify({"status": "error", "message": message}), 500


@app.route("/attack")
def p_attack():
    att.attack()


# Define the topic to which you want to consume messages
topic = "ecommerce_activity"

if __name__ == "__main__":
    lbf = LearnedBloomFilter(MODE.STREAM, ["127.0.0.1:9092", topic])
    app.run(host="0.0.0.0", port=5001, debug=True)
