from fastapi import FastAPI
import people_count_predict as pcp

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/predict/{place}")
async def predict(place: str):
    print("Hello")
    return pcp.predict(place)
