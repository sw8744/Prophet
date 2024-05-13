import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric

df = pd.read_excel(r"C:\Users\User\Desktop\서울시 인구 데이터.xlsx", engine="openpyxl")
print(df)
dataframe = DataFrame({
    'ds': df.time,
    'y': (df.ppl_min + df.ppl_max) / 2
})
prophet = Prophet(changepoint_prior_scale=0.05, daily_seasonality=True)
prophet.fit(dataframe)
future = prophet.make_future_dataframe(periods=5 * 12, freq="H")
forecast = prophet.predict(future)
forecast_df = DataFrame({
    'ds': forecast['ds'],
    'yhat': forecast['yhat'],
    'yhat_lower': forecast['yhat_lower'],
    'yhat_upper': forecast['yhat_upper']
})
print(forecast_df)
# prophet.plot(forecast, xlabel='Date', ylabel='people')
# plt.show()
cross_validation_results = cross_validation(prophet, initial='1 hours', period='1 hours', horizon='1 hours')
print(cross_validation_results)
performance_metrics_results = performance_metrics(cross_validation_results)
print(performance_metrics_results)
plot_cross_validation_metric(cross_validation_results, metric='mdape')
plt.ylim(0, 5)
plt.show()
print("hello world")
