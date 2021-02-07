import csv
import os
import sktime.forecasting.all as sk
import numpy as np


def get_os_filename(file_path, *args):
    if os.name == "nt":
        intermediate_dirs = ""
        for arg in args:
            intermediate_dirs = intermediate_dirs + arg + "\\"
        file_path_os = os.getcwd() + "\\" + intermediate_dirs + file_path

    elif os.name == "posix":
        intermediate_dirs = ""
        for arg in args:
            intermediate_dirs = intermediate_dirs + arg + "\\"
        file_path_os = os.getcwd() + "/" + intermediate_dirs + file_path
    else:
        raise NotImplementedError("Unsupported Operating System.")

    return file_path_os


def parser_csv_user(file_path):
    """
    Parse the csv in the "user" format and return its dictionary representation.

    :param file_path: Fully specified file_path.
    :return: dictionary representation of file that file_path points to.
    """

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        parsed_data = {}
        for row in reader:
            if row[0] == "day":
                for entry in row[1::]:
                    parsed_data[str(entry)] = {}
            elif row[0] == "start time":
                for entry in range(1, len(row)):
                    parsed_data[str(entry)]["start_time"] = str(row[entry])
            elif row[0] == "end time":
                for entry in range(1, len(row)):
                    parsed_data[str(entry)]["end_time"] = str(row[entry])
            elif row[0] == "quality of sleep (0 - 10)":
                for entry in range(1, len(row)):
                    parsed_data[str(entry)]["quality_of_sleep"] = int(row[entry])

    return parsed_data


def write_csv_user(file_path, data):
    """
    Writes the dictionary specified by data to the file contained in file_path

    :param file_path: fully specified file path.
    :param data: dictionary to be written to file path.
    :return: None.
    """

    days = list(data.keys())
    days.sort()
    attributes = data["1"].keys() # get the first entry
    attribute_rows = {}
    attribute_rows["day"] = days
    for attribute in attributes:
        attribute_rows[attribute] = []
    for day in days:
        for attribute in data[day]:
            attribute_rows[attribute].append(data[day][attribute])

    # TODO: why is the order inverted?
    days.reverse()
    attribute_rows["day"] = days

    # writing step
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for key in attribute_rows:
            writer.writerow([key] + attribute_rows[key])

    pass


def predict_sleep(user_history, new_data, time_forecast=None):
    """
    Given the user's historic sleep data and the new, voluntarily provided
    data, generate a new forecast for the user's sleep.

    :param user_history: historic user sleep data
    :param new_data: new data provided in this run of "predict_sleep"
    :param **kwargs:
        time_forecast: the length of the forecast is a max of seven days.
        If time_forecast is provided, this value overrides the forecast length
        (up to a max of seven days)
    :return: the sleep_forecast
    """
    forecast_length = len(new_data)
    if time_forecast:
        forecast_length = time_forecast
    forecast_length = min(forecast_length, 7)

    # generate a relative forecasting horizon
    rfh = np.arange(forecast_length) + 1

    # Specify the model
    forecaster = sk.ExponentialSmoothing(trend="add", seasonal="multiplicative", sp=7)

    # fit it to the user_history
    forecaster.fit(user_history)

    # generate a prediction
    sleep_forecast = forecaster.predict(rfh)

    return sleep_forecast




if __name__ == '__main__':
    """ Run through the usage of sleep_stats"""
    file_name = "/test/test_inputs/sample_7_days.csv"
    user_entries = parser_csv_user(os.getcwd() + file_name)

    print(user_entries)
