import people_count_predict as pcp
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return jsonify({"message": "Hello World!"})


@app.route("/predict/<place>")
def predict(place):
    result = pcp.predict(place.replace("+", " "))
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
