import argparse
import sleep_stats.forecast
import sleep_stats.visualization
import os


def init():
    print("Creating new directory for user defined data...")
    os.makedirs(os.getcwd() + '/default')
    exit()


def start_program():
    if not os.path.isdir(os.getcwd() + '/default'):
        init()

    # define name_space
    name_space = {"historical_data_location": os.getcwd() + "/default/user_history.csv",
                  "new_user_data_location": os.getcwd() + "/default/new_user_data.csv"}

    # use argparse to determine the user inputs/configs
    parser = argparse.ArgumentParser(description='Track and predict sleep quality.',
                                     usage='Use this program to track your sleep and predict your sleep quality.\n'
                                           '\n'
                                           'Usage: sleep_stats [-d "path/to/custom_user_history.csv"] '
                                           '[-u "path/to/custom_recent_sleep_data.csv\n'
                                           '\n'
                                           'By default, sleep_stats stores its user preferences in the /default'
                                           'folder.\n',
                                     )

    # optional arguments
    parser.add_argument('-u', '--user')
    parser.add_argument('-d', '--directory')

    # obtain user inputted values
    name_space_temp = parser.parse_args()
    # TODO: replace defaults with optional arguments

    # for now: assume defaults
    hist_time_date, hist_quality_date = sleep_stats.forecast.read_data(name_space["historical_data_location"])
    # read in (optional) user data
    user_time_date, user_quality_date = sleep_stats.forecast.read_data(
        name_space["new_user_data_location"],
        is_user=True
    )

    # only care about time, date relationship!
    merged_data = sleep_stats.forecast.merge_data(hist_time_date, user_time_date)
    # state machine
    predictions = sleep_stats.forecast.run_forecast(merged_data, len(user_time_date.index))

    print("Predictions made.")
    sleep_stats.forecast.save_data(os.getcwd() + "/default/predictions.csv", predictions)


if __name__ == '__main__':
    start_program()
else:
    raise NotImplementedError("main.py cannot be used as an API")
