import json
from prophet import Prophet
from pandas import DataFrame
import logging
import requests
import pandas as pd
from datetime import datetime
import schedule
import time
import pymysql


conn = pymysql.connect(host="app.ishs.co.kr", user="", password="", db="people", charset="utf8")
curs = conn.cursor()

logger = logging.getLogger('cmdstanpy')
logger.addHandler(logging.NullHandler())
logger.propagate = False
logger.setLevel(logging.CRITICAL)

people_data: dict = {}
predict_data: dict = {}

df = pd.read_csv('./places.csv')

AREA_CD = df['AREA_CD'].tolist()
AREA_NM = df['AREA_NM'].tolist()
AREA_SIZE = df['AREA_SIZE'].tolist()
ADDRESS = df['ADDRESS'].tolist()


def get_data(place):
    curs.execute(f"SELECT * FROM people WHERE place_name='{place}'")
    rows = curs.fetchall()
    return rows


def init_people_data(key: str):
    global people_data
    ppl_list = []
    day_list = []
    for ppl_data in get_data(key):
        max_ppl = ppl_data[3]
        min_ppl = ppl_data[2]
        ppl_mean = (max_ppl + min_ppl) / 2
        ppl_list.append(ppl_mean)
        day_list.append(ppl_data[1].strftime("%Y-%m-%d %H:%M:%S"))
        data = {
            "ds": day_list,
            "y": ppl_list
        }
        people_data[key] = DataFrame(data)
    print("done")


def update_people_data(place, time, amount):
    global people_data
    data = {
        "ds": time,
        "y": amount
    }
    people_data[place] = people_data[place].append(data, ignore_index=True)
    print("update")


def predict_people_count(place):
    prophet = Prophet(changepoint_prior_scale=0.15, daily_seasonality=True)
    prophet.fit(people_data[place])

    fcast_time = 13
    future = prophet.make_future_dataframe(periods=fcast_time, freq="5T")
    print(future.tail(13))

    forecast = prophet.predict(future).tail(13)

    forecast_data = {
        'ds': forecast['ds'],
        'yhat': forecast['yhat'],
        'yhat_lower': forecast['yhat_lower'],
        'yhat_upper': forecast['yhat_upper']
    }

    forecast_df = DataFrame(forecast_data)
    print(forecast_df)
    forecast_json = forecast_df.to_json(orient='columns')
    print(forecast_json)
    return forecast_data


def send(placeNM):
    host = f"http://openapi.seoul.go.kr:8088/4e574f4441796f7537316758474875/json/citydata_ppltn/1/5/{AREA_CD[AREA_NM.index(placeNM)]}"
    res = requests.get(host)
    print(res.text)
    data = json.loads(res.text)
    AREA_PPLTN_MIN = data['SeoulRtd.citydata_ppltn'][0]['AREA_PPLTN_MIN']
    AREA_PPLTN_MAX = data['SeoulRtd.citydata_ppltn'][0]['AREA_PPLTN_MAX']
    print(f"{placeNM}의 현재 인구는 {AREA_PPLTN_MIN} ~ {AREA_PPLTN_MAX}명 입니다.")
    return {
        "AREA_NM": placeNM,
        "AREA_PPLTN_MIN": int(AREA_PPLTN_MIN),
        "AREA_PPLTN_MAX": int(AREA_PPLTN_MAX)
    }


def predict(place):
    if place not in people_data:
        init_people_data(place)
    people = send(place)
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_people_data(place, t, (people['AREA_PPLTN_MIN'] + people['AREA_PPLTN_MAX']) // 2)
    predict_data[place] = predict_people_count(place)
    print(predict_data[place])
    return predict_data[place]


def predict_all():
    for place in AREA_NM:
        predict(place)
