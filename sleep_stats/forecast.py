import pandas as pd
import os
import numpy as np
from sktime.forecasting import all as sk
from sktime.forecasting.all import *
from sktime.forecasting.ets import AutoETS



def read_data(target_dir, is_user=False):
    def raise_minimum(x):
        if isinstance(x, int):
            if x == 0:
                return 1
            else:
                return x
        elif isinstance(x, float):
            if x <= 0.0:
                return 0.1
            else:
                return x
        else:
            raise ValueError()

    df = pd.read_csv(target_dir)
    # (1) in case the user provides 0.0 as an entry, which may
    # break Holt-Winters predictions currently being used.
    # https://stats.stackexchange.com/questions/90079/why-multiplicative-holt-winters-requires-strictly-positive-data-points
    df['Sleep quality'] = df['Sleep quality'].apply(raise_minimum)
    df['Time in bed'] = df['Time in bed'].apply(raise_minimum)
    date_quality_df = df.iloc[:, 0:2]
    date_time_df = df.iloc[:, 0:3:2]
    # serialize
    date_time_df.set_index('Date', inplace=True)
    # date_time_df = date_time_df.iloc[:,0] + date_time_df.iloc[:,2:]
    # print(date_time_df)
    date_quality_df.set_index('Date', inplace=True)
    date_time_s = date_time_df.squeeze()
    date_quality_s = date_quality_df.squeeze()

    date_time_s.name = "Sleep time in minutes"
    date_time_s.index = pd.PeriodIndex(date_time_s.index, freq="D", name="Period")

    date_quality_s.name = "Sleep quality from 0.1 to 10.0"
    date_quality_s.index = pd.PeriodIndex(date_time_s.index, freq="D", name="Period")

    return date_time_s, date_quality_s


def save_data(target_dir, data_s):
    data_df = data_s.to_frame()
    data_df = data_df.rename(columns={0: "Sleep Quality"})
    data_df.to_csv(target_dir)


def run_forecast(train_df, forecast_horizon):
    # generate a forecasting horizon
    r_sleep_fh = np.arange(forecast_horizon) + 1
    # afh = ForecastingHorizon(forecast_horizon, is_relative=False)

    # specify the model
    # forecast = AutoETS(auto=True, sp=7, n_jobs=-1)
    forecast = sk.ExponentialSmoothing(trend="add", seasonal="multiplicative", sp=2*forecast_horizon)
    # fit it to the training data
    forecast.fit(train_df)
    # generate a prediction
    prediction = forecast.predict(r_sleep_fh)

    return prediction


def merge_data(data_head, data_tail):
    return data_head.append(data_tail)
