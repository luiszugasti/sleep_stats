import unittest

import sleep_stats as dc


class TestParser(unittest.TestCase):
    def test_data_read_correctly(self):
        """
        With a regular data entry, test that
        it is read properly to the correct data representation
        """
        correct_repr = {'7': {'start_time': '9pm', 'end_time': '8am', 'quality_of_sleep': 8},
                        '6': {'start_time': '3am', 'end_time': '6am', 'quality_of_sleep': 0},
                        '5': {'start_time': '10pm', 'end_time': '7am', 'quality_of_sleep': 6},
                        '4': {'start_time': '9pm', 'end_time': '7am', 'quality_of_sleep': 7},
                        '3': {'start_time': '9pm', 'end_time': '6am', 'quality_of_sleep': 7},
                        '2': {'start_time': '8pm', 'end_time': '7am', 'quality_of_sleep': 6},
                        '1': {'start_time': '9pm', 'end_time': '7am', 'quality_of_sleep': 7}}
        file_path = dc.get_os_filename("sample_7_days.csv", "test_inputs")
        comparison_repr = dc.parser_csv_user(file_path)

        self.assertEqual(correct_repr, comparison_repr)

    def test_output_data_correctly(self):
        """
        With a predefined output data format,
        test that it is written to a file, and that the data within is correct.
        """
        sample_repr = {'7': {'start_time': '9pm', 'end_time': '8am', 'quality_of_sleep': 8},
                       '6': {'start_time': '3am', 'end_time': '6am', 'quality_of_sleep': 0},
                       '5': {'start_time': '10pm', 'end_time': '7am', 'quality_of_sleep': 6},
                       '4': {'start_time': '9pm', 'end_time': '7am', 'quality_of_sleep': 7},
                       '3': {'start_time': '9pm', 'end_time': '6am', 'quality_of_sleep': 7},
                       '2': {'start_time': '8pm', 'end_time': '7am', 'quality_of_sleep': 6},
                       '1': {'start_time': '9pm', 'end_time': '7am', 'quality_of_sleep': 7}}

        file_path = dc.get_os_filename("sample_test_output.csv", "test_output")
        dc.write_csv_user(file_path, sample_repr)

        comparison_repr = dc.parser_csv_user(file_path)

        self.assertEqual(comparison_repr, dc.parser_csv_user(file_path))

    def test_correct_error_raised(self):
        """
        Test that different kinds of errors are raised
        correctly.
        """
        # TODO: stub
        pass


class TestFileOpener(unittest.TestCase):
    def test_correct_file_found(self):
        """
        Test that when provided a file name, the correct file
        is found
        """
        # TODO: stub
        pass

    def test_file_written(self):
        """
        Test that when provided an output file name, it is
        written to that directory.
        Additionally, the correct error is raised when the
        file cannot be written.
        """
        # TODO: stub
        pass
