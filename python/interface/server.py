"""
@author Aaditya
@version 0.1
@since 17-03-2024
This file maps the learned bloom filter APIs to REST API endpoints.
USE IN REST MODE ONLY
"""
from flask import Flask, request, jsonify
from api import LearnedBloomFilter, MODE
<<<<<<< HEAD
=======
from Attacker import attacker
>>>>>>> master

app = Flask(__name__)


@app.route("/")
def base():
    return


@app.route("/insert", methods=["POST"])
def insert():
    data = request.get_json()
<<<<<<< HEAD
    lbf.insert(data.key)
    # TODO: call to insert into DB
    return 201
=======
    lbf.insert(int(data['key']))
    return '', 201
>>>>>>> master


@app.route("/query/<key>")
def query(key):
<<<<<<< HEAD
    result = lbf.query(int(key))
    json_result = {
        "Present": result
    }
    return jsonify(json_result), 200
=======
    found = False
    result = lbf.query(int(key))
    return result, 200
>>>>>>> master


@app.route("/consume")
def consume():
    lbf.consume()


<<<<<<< HEAD
if __name__ == "__main__":
    lbf = LearnedBloomFilter(MODE.STREAM, ['localhost:9092', 'stream-test'])
=======
@app.route("/attack")
def p_attack():
    att.attack()


if __name__ == "__main__":
    lbf = LearnedBloomFilter(MODE.STREAM, ['localhost:9092', 'stream-test'])
    att = attacker.Attacker()
>>>>>>> master
    app.run(debug=True)
