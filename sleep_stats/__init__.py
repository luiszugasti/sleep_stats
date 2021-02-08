import csv
import pandas as pd
import numpy as np
import os
import sktime.forecasting.all as sk


def get_os_filename(file_name, *args):
    """
        UN-USED API - Still figuring out what it will be used for.
    :param file_name: File name, including extension, to the file you wish to use.
    :param args: sequential, continual in-depth folders until we get to your file.
    :return:
    """
    print("WARNING: This API has been deprecated and may go out of use!")
    if os.name == "nt":
        intermediate_dirs = ""
        for arg in args:
            intermediate_dirs = intermediate_dirs + arg + "\\"
        file_path_os = os.getcwd() + "\\" + intermediate_dirs + file_name

    elif os.name == "posix":
        intermediate_dirs = ""
        for arg in args:
            intermediate_dirs = intermediate_dirs + arg + "/"
        file_path_os = os.getcwd() + "/" + intermediate_dirs + file_name
    else:
        raise NotImplementedError("Unsupported Operating System.")

    return file_path_os


def parser_csv_user(file_path):
    """
    UN-USED API - Will likely be removed, pandas does a better job.
    Parse the csv in the "user" format and return its dictionary representation.

    :param file_path: Fully specified file_path.
    :return: dictionary representation of file that file_path points to.
    """

    print("WARNING: This API has been deprecated and may go out of use!\n"
          "Please use sleep_data.forecast.read_data()")
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

    return parsed_data, len(parsed_data)


def write_csv_user(file_path, data):
    """
    UN-USED API - Will likely be removed, pandas does a better job.
    Writes the dictionary specified by data to the file contained in file_path

    :param file_path: fully specified file path.
    :param data: dictionary to be written to file path.
    :return: None.
    """
    print("WARNING: This API has been deprecated and may go out of use!\n"
          "Please use sleep_stats.forecast.save_data()")

    days = list(data.keys())
    days.sort()
    attributes = data["1"].keys()  # get the first entry
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
    UN-USED API - Will likely be removed, forecast.
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
    print("WARNING: This API has been deprecated and may go out of use!\n"
          "Please use sleep_stats.forecast.run_forecast()")
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


def main():
    """
    Deprecated - will be removed once tests pass on __main__.py's functions
    :return:
    """
    # Run through the usage of sleep_stats
    file_name = input("Enter the name of your sleep csv file: ")
    user_entries, num_entries = parser_csv_user(file_name)
    # Load the users prior data
    sleepArray, timeInBedArray = dataLoader()

    forecast = predict_sleep(sleepArray, user_entries, num_entries)
    print(forecast)
    return forecast


def dataLoader():
    print("WARNING: This API has been deprecated and may go out of use!\n"
          "The schema referred to by this API is no longer in use.")
    df = pd.read_csv("data/sleepdata.csv")  # may need to add os.getcwd() if on windows machine
    # Drop extraneous columns not used in analysis
    df = df.drop('Heart rate', 1)
    df = df.drop('Activity (steps)', 1)
    df = df.drop('Sleep Notes', 1)
    df = df.drop('Wake up', 1)
    df = df.drop('End', 1)
    # Edit below data to fit appropriate constraints
    df['Sleep quality'] = df['Sleep quality'].apply(truncate_percentage_to_range)
    df['Time in bed'] = df['Time in bed'].apply(time_to_minutes)
    df['Start'] = df['Start'].apply(extract_date)
    df = df.rename(columns={'Start': 'Date'})

    # Obtain user data
    user_df = pd.read_csv("test/test_inputs/sample_7_days.csv")  # may need to add os.getcwd() if on windows machine
    user_df["Time in bed"] = 60 * user_df["Time in bed"]

    # Append user data to test
    result = df.append(user_df)
    sleepArray = result.iloc[:, 0:2]
    timeInBedArray = result[['Date', 'Time in bed']]
    print(sleepArray)
    print(timeInBedArray)
    return sleepArray, timeInBedArray


# Helper functions for modifying the data to fit the correct format
def truncate_percentage_to_range(x):
    x = x.strip('%')
    x = int(x) / 10.0
    return x


def time_to_minutes(x):
    s = x.split(":")
    s = int(s[0]) * 60 + int(s[1])
    return s


def extract_date(x):
    s = x.split(" ")
    return s[0]


if __name__ == '__main__':
    """ Run through the usage of sleep_stats"""
    main()
