import unittest

from datacollab import parser_csv_user
from datacollab import file_opener

class TestParser(unittest.TestCase):
    def test_data_read_correctly(self):
        """
        With a regular data entry, test that
        it is read properly to the correct data representation
        """
        # TODO: stub
        pass

    def test_output_data_correctly(self):
        """
        With a predefined output data format,
        test that it is written properly to a csv file.
        """
        # TODO: stub
        pass

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





