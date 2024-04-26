"""
@author Aaditya
@version 0.1
@since 17-03-2024
This file maps the learned bloom filter APIs to REST API endpoints.
USE IN REST MODE ONLY
"""
from flask import Flask, request, jsonify
from api import LearnedBloomFilter, MODE
from Attacker import attacker

app = Flask(__name__)


@app.route("/")
def base():
    return


@app.route("/insert", methods=["POST"])
def insert():
    data = request.get_json()
    lbf.insert(int(data['key']))
    return '', 201


@app.route("/query/<key>")
def query(key):
    found = False
    result = lbf.query(int(key))
    return result, 200


@app.route("/consume")
def consume():
    lbf.consume()


@app.route("/attack")
def p_attack():
    att.attack()


if __name__ == "__main__":
    lbf = LearnedBloomFilter(MODE.STREAM, ['localhost:9092', 'stream-test'])
    att = attacker.Attacker()
    app.run(debug=True, threaded=True)
