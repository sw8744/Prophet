from fbprophet import Prophet
from pandas import DataFrame
import logging
import pandas as pd
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt

logger = logging.getLogger('cmdstanpy')
logger.addHandler(logging.NullHandler())
logger.propagate = False
logger.setLevel(logging.CRITICAL)

plt.figure(dpi=300)

df = pd.read_csv('./wavedata.csv')

wave_height = df['파고[m]'].tolist()
wave_height_max = df['최대파고[m]'].tolist()


def create_date_list():
    date_list = []
    datetime1 = datetime(2016, 1, 1, 0, 0, 0)
    for i in range(0, len(wave_height)):
        datetime1 = datetime1 + timedelta(hours=1)
        date_list.append(datetime1.strftime("%Y-%m-%d %H:%M:%S"))
    print(date_list)
    return date_list


def predict_wave_height():
    dataframe = DataFrame({
        'ds': create_date_list(),
        'y': wave_height
    })
    prophet = Prophet(changepoint_prior_scale=0.15, daily_seasonality=True)
    prophet.fit(dataframe)
    future = prophet.make_future_dataframe(periods=24, freq="H")
    forecast = prophet.predict(future).tail(24)
    forecast_df = DataFrame({
        'ds': forecast['ds'],
        'yhat': forecast['yhat'],
        'yhat_lower': forecast['yhat_lower'],
        'yhat_upper': forecast['yhat_upper']
    })
    print(forecast_df)
    prophet.plot(forecast)
    plt.show()


predict_wave_height()