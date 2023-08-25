from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
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
    prophet = Prophet(changepoint_prior_scale=0.05, daily_seasonality=True)
    prophet.fit(dataframe)
    future = prophet.make_future_dataframe(periods=24 * 30, freq="H")
    forecast = prophet.predict(future)
    forecast_df = DataFrame({
        'ds': forecast['ds'],
        'yhat': forecast['yhat'],
        'yhat_lower': forecast['yhat_lower'],
        'yhat_upper': forecast['yhat_upper']
    })
    print(forecast_df)
    prophet.plot(forecast, xlabel='Date', ylabel='Wave Height(m)')
    plt.show()
    cross_validation_results = cross_validation(prophet, initial=f'{24 * 30} hours', period='48 hours', horizon=f'{24 * 10} hours')
    print(cross_validation_results)
    performance_metrics_results = performance_metrics(cross_validation_results)
    print(performance_metrics_results)
    plot_cross_validation_metric(cross_validation_results, metric='mape')
    plt.ylim(0, 5)
    plt.show()


def main():
    predict_wave_height()


if __name__ == '__main__':
    main()
