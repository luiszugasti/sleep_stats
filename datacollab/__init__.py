import csv
import os


def parser_csv_user(file_path):

    if os.name == "nt":
        file_path_os = os.getcwd() + "\\" + file_path
    elif os.name == "posix":
        file_path_os = os.getcwd() + "/" + file_path
    else:
        raise NotImplementedError("Unsupported Operating System.")

    with open(file_path_os, newline='') as csvfile:
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


if __name__ == '__main__':
    """ Run through the usage of datacollab"""
    file_name = "Sample Format.csv"
    user_entries = parser_csv_user(file_name)

    print(user_entries)
