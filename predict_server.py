from fastapi import FastAPI
import people_count_predict as pcp
from fastapi.middleware.cors import CORSMiddleware
import update_db as udb
import multiprocessing as mp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/predict/{place}")
async def predict(place: str):
    print("Hello")
    return pcp.predict_data[place.replace("+", " ")]


if __name__ == "__main__":
    import uvicorn
    p1 = mp.Process(target=udb.update)
    p1.start()
    p2 = mp.Process(target=pcp.update)
    p2.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
