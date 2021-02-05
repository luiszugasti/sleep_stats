import pandas as pd
import numpy as np
import os

def main():
    df = pd.read_csv("data/sleepdata.csv") # may need to add os.getcwd() if on windows machine
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
    df = df.rename(columns={'Start':'Date'})    

    # Obtain user data
    user_df = pd.read_csv("test/test_inputs/sample_7_days.csv") # may need to add os.getcwd() if on windows machine
    user_df["Time in bed"] = 60 * user_df["Time in bed"]

    # Append user data to test
    result = df.append(user_df)
    sleepArray = result.iloc[:, 0:2]
    timeInBedArray = result[['Date','Time in bed']]
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
    main()
