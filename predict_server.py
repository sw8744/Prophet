import people_count_predict as pcp
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return {"message": "Hello World!"}


@app.route("/predict/<str:place>")
def predict(place: str):
    return pcp.predict(place.replace("+", " "))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
