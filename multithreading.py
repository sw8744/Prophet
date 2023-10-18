import threading
import time
import schedule
import queue
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_list = {}
q = queue.Queue()


def add_data(key):
    global data_list
    data_list[key] = "Hello World!"


def add_all_data():
    key_list = ["a", "b", "c", "d", "e"]
    for key in key_list:
        add_data(key)
    print("done")


@app.get("/")
def get_data():
    global data_list
    return data_list


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    import uvicorn
    schedule.every(5).seconds.do(run_threaded, add_all_data)
    p1 = threading.Thread(target=run_schedule)
    p1.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)

