import csv
import os


def get_os_filename(file_path, *args):
    file_path_os = ""

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
    pass


if __name__ == '__main__':
    """ Run through the usage of datacollab"""
    file_name = "Sample Format.csv"
    user_entries = parser_csv_user(file_name)

    print(user_entries)
