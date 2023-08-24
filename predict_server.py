from fastapi import FastAPI
import people_count_predict as pcp

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/predict/{place}")
async def predict(place: str):
    print("Hello")
    return pcp.predict(place.replace("+", " "))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
