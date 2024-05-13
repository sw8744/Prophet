from datetime import datetime
import pymysql
import logging
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric


conn = pymysql.connect(host="ishs.co.kr", user="root", password="ishs123!", db="kcf", charset="utf8")
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

cv_result = DataFrame()


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


def predict_people_count(place):
    global cv_result
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
    cross_validation_results = cross_validation(prophet, horizon='1 hours')
    print(cross_validation_results)
    performance_metrics_results = performance_metrics(cross_validation_results)
    print(performance_metrics_results)
    cv_result = performance_metrics_results
    plot_cross_validation_metric(cross_validation_results, metric='mdape')
    plt.ylim(0, 5)
    plt.show()
    return forecast_data


def predict_people(place):
    global predict_data
    if place not in people_data:
        init_people_data(place)
    predict_data[place] = predict_people_count(place)
    print(predict_data[place])
    return predict_data[place]


def predict_all():
    for place in AREA_NM:
        predict_people(place)


def get_data(place):
    curs.execute(f"SELECT * FROM people WHERE place_name='{place}'")
    rows = curs.fetchall()
    return rows


if __name__ == "__main__":
    init_people_data("경복궁")
    predict_people("경복궁")




