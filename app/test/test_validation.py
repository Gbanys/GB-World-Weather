import unittest
from src.validation.main_validation import check_if_graph_data_is_valid

class TestGraphValidation(unittest.TestCase):

    def test_unknown_city(self) -> None:
        city = 'Does not exist'
        startTime = '2023-01-11'
        endTime = '2023-01-17'
        expected_result = "Please enter a valid city name"
        actual_result = check_if_graph_data_is_valid(city, startTime, endTime)
        self.assertEqual(expected_result, actual_result)

    def test_start_time_in_wrong_format(self) -> None:
        city = 'London'
        startTime = '01/04/2023'
        expected_result = "Please enter the start date in the correct format (YYYY-MM-dd)"
        actual_result = check_if_graph_data_is_valid(city, startTime, endTime=None)
        self.assertEqual(expected_result, actual_result)

    def test_end_time_in_wrong_format(self) -> None:
        city = 'London'
        endTime = '01/04/2023'
        expected_result = "Please enter the end date in the correct format (YYYY-MM-dd)"
        actual_result = check_if_graph_data_is_valid(city, None, endTime)
        self.assertEqual(expected_result, actual_result)

    def test_end_time_without_start_time(self) -> None:
        city = 'London'
        endTime = '2023-01-04'
        expected_result = "Please specify the start date if you have specified the end date"
        actual_result = check_if_graph_data_is_valid(city, None, endTime)
        self.assertEqual(expected_result, actual_result)

    def test_start_date_later_than_end_date(self) -> None:
        city = 'London'
        startTime = '2023-01-17'
        endTime = '2023-01-11'
        expected_result = "Dates are invalid, make sure that start date is earlier than end date"
        actual_result = check_if_graph_data_is_valid(city, startTime, endTime)
        self.assertEqual(expected_result, actual_result)

    def test_all_valid_data(self) -> None:
        city = 'London'
        startTime = '2023-01-11'
        endTime = '2023-01-17'
        expected_result = ""
        actual_result = check_if_graph_data_is_valid(city, startTime, endTime)
        self.assertEqual(expected_result, actual_result)


if __name__ == '__main__':
    unittest.main()