import people_count_predict as pcp
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return {"message": "Hello World!"}


@app.route("/predict/<str:place>")
def predict(place: str):
    return pcp.predict(place.replace("+", " "))
