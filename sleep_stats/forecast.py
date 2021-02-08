import pandas as pd
import numpy as np
from sktime.forecasting import all as sk
import datetime


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

    date_quality_df.set_index('Date', inplace=True)
    date_time_s = date_time_df.squeeze()
    date_quality_s = date_quality_df.squeeze()

    date_time_s.name = "Sleep time in minutes"
    date_time_s.index = pd.PeriodIndex(date_time_s.index, freq="D", name="Period")

    date_quality_s.name = "Sleep quality from 0.1 to 10.0"
    date_quality_s.index = pd.PeriodIndex(date_time_s.index, freq="D", name="Period")

    if is_user:
        # convert from hours to minutes
        date_time_s = 60 * date_time_s
    return date_time_s, date_quality_s


def save_data(target_dir, data_s):
    # generate days to fill
    base_day = datetime.datetime.today()
    date_list = [base_day + datetime.timedelta(days=x) for x in range(len(data_s.index))]
    date_string_list = ["{}-{}-{}".format(x.month, x.day, x.year) for x in date_list]
    # dates_df = pd.DataFrame(date_list)

    data_df = data_s.to_frame()
    data_df['Date'] = date_string_list
    data_df = data_df.rename(columns={0: "Hours of Sleep"})
    data_df.set_index("Date", inplace=True)
    data_df.to_csv(target_dir)


def run_forecast(train_df, forecast_horizon):
    """
    Given the user's historic sleep data (@train_df) and a forecast_horizon,
    data, generate a new forecast for the user's sleep time in hours.

    :param train_df: The data frame to train the model on.
    :param forecast_horizon: The length of time to generate a forecast. Can be any number, however, only a max of
        7 days will be forecast.
    :return: The predictions of sleep.
    """

    # generate a forecasting horizon
    r_sleep_fh = np.arange(forecast_horizon) + 1

    # specify the model
    forecast = sk.ExponentialSmoothing(trend="add", seasonal="multiplicative", sp=7)
    # fit it to the training data
    forecast.fit(train_df)
    # generate a prediction
    prediction = forecast.predict(r_sleep_fh)

    # clamp predictions to hours.
    prediction = prediction // 60

    return prediction


def merge_data(data_head, data_tail):
    return data_head.append(data_tail, ignore_index=True)
