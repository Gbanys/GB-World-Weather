import unittest
import pandas as pd
from database_service.src.weather_alarms import retrieve_required_messages_and_phone_numbers
from unittest.mock import patch

class TestWeatherAlarmService(unittest.TestCase):

    @patch('data_access.weather_api.weather_api.get_weather_data_from_api')
    def test_retrieve_weather_events_from_one_subscriber(self, mock_weather_api):

        mock_weather_api.get_weather_data_from_api.return_value = {
            'hourly' : {'weather_code' : [0, 0, 2, 2, 3, 2, 1],
                        'time' : ['2023-11-18T10:00', '2023-11-18T11:00', '2023-11-18T12:00', '2023-11-18T13:00', '2023-11-18T14:00', '2023-11-18T15:00', '2023-11-18T16:00'],
                        'is_day' : [1, 1, 1, 1, 1, 1, 1],
                        'temperature_2m' : [9.4, 10.2, 11.5, 12.1, 12.5, 11.4, 10.3],
                        'precipitation_probability' : [23, 30, 38, 64, 71, 40, 21],
                        'wind_speed_10m' : [10.4, 11.5, 12.4, 14.0, 12.1, 11.3, 9.4]
                       },
            'current' : {'time' : '2023-11-18T10:00'}
        }

        data = {'id': {0: 1},
        'firstname': {0: 'John'},
        'lastname': {0: 'Doe'},
        'phone_number': {0: '1234567'},
        'city': {0: 'London'},
        'weather_event': {0: 'overcast'},
        'metric': {0: None},
        'metric_limit': {0: None},
        'notify_before': {0: 5}}

        subscriber_dataframe = pd.DataFrame(data)
        
        expected_result = {'1234567' : {"new_weather_event" : "Hello. This is a notification from world weather forecast. overcast weather is expected on 2023-11-18 14:00:00"}}
        actual_result = retrieve_required_messages_and_phone_numbers(subscriber_dataframe, mock_weather_api)

        self.assertEqual(expected_result, actual_result)


    @patch('data_access.weather_api.weather_api.get_weather_data_from_api')
    def test_retrieve_weather_events_from_multiple_subscribers(self, mock_weather_api):

        mock_weather_api.get_weather_data_from_api.return_value = {
            'hourly' : {'weather_code' : [0, 0, 2, 2, 3, 2, 1],
                        'time' : ['2023-11-18T10:00', '2023-11-18T11:00', '2023-11-18T12:00', '2023-11-18T13:00', '2023-11-18T14:00', '2023-11-18T15:00', '2023-11-18T16:00'],
                        'is_day' : [1, 1, 1, 1, 1, 1, 1],
                        'temperature_2m' : [9.4, 10.2, 11.5, 12.1, 12.5, 11.4, 10.3],
                        'precipitation_probability' : [23, 30, 38, 64, 71, 40, 21],
                        'wind_speed_10m' : [10.4, 11.5, 12.4, 14.0, 12.1, 11.3, 9.4]
                       },
            'current' : {'time' : '2023-11-18T10:00'}
        }

        data = {'id': {0: 1, 1: 2, 2: 3},
        'firstname': {0: 'John', 1: 'John', 2: 'John'},
        'lastname': {0: 'Doe', 1: 'Doe', 2: 'Doe'},
        'phone_number': {0: '1234567', 1: '1234568', 2: '1234569'},
        'city': {0: 'London', 1: 'London', 2: 'London'},
        'weather_event': {0: 'overcast', 1: 'cloudy', 2: 'sunny'},
        'metric': {0: None, 1: None, 2: None},
        'metric_limit': {0: None, 1: None, 2: None},
        'notify_before': {0: 5, 1: 5, 2: 3}
        }

        subscriber_dataframe = pd.DataFrame(data)
        
        expected_result = { 
            '1234567' : {'new_weather_event' : "Hello. This is a notification from world weather forecast. overcast weather is expected on 2023-11-18 14:00:00"},
            '1234568' : {'new_weather_event' : "Hello. This is a notification from world weather forecast. cloudy weather is expected on 2023-11-18 12:00:00"},
            '1234569' : {'new_weather_event' : "Hello. This is a notification from world weather forecast. sunny weather is expected on 2023-11-18 10:00:00"}
        }

        actual_result = retrieve_required_messages_and_phone_numbers(subscriber_dataframe, mock_weather_api)

        self.assertEqual(expected_result, actual_result)


    @patch('data_access.weather_api.weather_api.get_weather_data_from_api')
    def test_retrieve_metrics_from_one_subscriber(self, mock_weather_api):

        mock_weather_api.get_weather_data_from_api.return_value = {
            'hourly' : {'weather_code' : [0, 0, 2, 2, 3, 2, 1],
                        'time' : ['2023-11-18T10:00', '2023-11-18T11:00', '2023-11-18T12:00', '2023-11-18T13:00', '2023-11-18T14:00', '2023-11-18T15:00', '2023-11-18T16:00'],
                        'is_day' : [1, 1, 1, 1, 1, 1, 1],
                        'temperature_2m' : [9.4, 10.2, 11.5, 12.1, 12.5, 11.4, 10.3],
                        'precipitation_probability' : [23, 30, 38, 64, 71, 40, 21],
                        'wind_speed_10m' : [10.4, 11.5, 12.4, 14.0, 12.1, 11.3, 9.4]
                       },
            'current' : {'time' : '2023-11-18T10:00'}
        }

        data = {'id': {0: 1},
        'firstname': {0: 'John'},
        'lastname': {0: 'Doe'},
        'phone_number': {0: '1234567'},
        'city': {0: 'London'},
        'weather_event': {0: None},
        'metric': {0: 'temperature_2m'},
        'metric_limit': {0: 12},
        'notify_before': {0: 5}}

        subscriber_dataframe = pd.DataFrame(data)
        
        expected_result = {'1234567' : {"exceeded_metric" : "Hello. This is a notification from world weather forecast. Your selected temperature_2m\
                  will be exceeded on 2023-11-18 13:00:00. temperature_2m will be 12.1 at this time"}}
        actual_result = retrieve_required_messages_and_phone_numbers(subscriber_dataframe, mock_weather_api)

        self.assertEqual(expected_result, actual_result)


    @patch('data_access.weather_api.weather_api.get_weather_data_from_api')
    def test_retrieve_metrics_from_multiple_subscriber(self, mock_weather_api):

        mock_weather_api.get_weather_data_from_api.return_value = {
            'hourly' : {'weather_code' : [0, 0, 2, 2, 3, 2, 1],
                        'time' : ['2023-11-18T10:00', '2023-11-18T11:00', '2023-11-18T12:00', '2023-11-18T13:00', '2023-11-18T14:00', '2023-11-18T15:00', '2023-11-18T16:00'],
                        'is_day' : [1, 1, 1, 1, 1, 1, 1],
                        'temperature_2m' : [9.4, 10.2, 11.5, 12.1, 12.5, 11.4, 10.3],
                        'precipitation_probability' : [23, 30, 38, 64, 71, 40, 21],
                        'wind_speed_10m' : [10.4, 11.5, 12.4, 14.0, 12.1, 11.3, 9.4]
                       },
            'current' : {'time' : '2023-11-18T10:00'}
        }

        data = {'id': {0: 1, 1: 2, 2: 3},
        'firstname': {0: 'John', 1: 'John', 2: 'John'},
        'lastname': {0: 'Doe', 1: 'Doe', 2: 'Doe'},
        'phone_number': {0: '1234567', 1: '1234568', 2: '1234569'},
        'city': {0: 'London', 1: 'London', 2: 'London'},
        'weather_event': {0: None, 1: None, 2: None},
        'metric': {0: 'temperature_2m', 1: 'precipitation_probability', 2: 'wind_speed_10m'},
        'metric_limit': {0: 10.0, 1: 70, 2: 12},
        'notify_before': {0: 5, 1: 5, 2: 3}
        }

        subscriber_dataframe = pd.DataFrame(data)
        
        expected_result = {'1234567' : {"exceeded_metric" : "Hello. This is a notification from world weather forecast. Your selected temperature_2m\
                  will be exceeded on 2023-11-18 11:00:00. temperature_2m will be 10.2 at this time"},
                  '1234568' : {"exceeded_metric" : "Hello. This is a notification from world weather forecast. Your selected precipitation_probability\
                  will be exceeded on 2023-11-18 14:00:00. precipitation_probability will be 71 at this time"},
                  '1234569' : {"exceeded_metric" : "Hello. This is a notification from world weather forecast. Your selected wind_speed_10m\
                  will be exceeded on 2023-11-18 12:00:00. wind_speed_10m will be 12.4 at this time"}
                  }
        actual_result = retrieve_required_messages_and_phone_numbers(subscriber_dataframe, mock_weather_api)

        self.assertEqual(expected_result, actual_result)



if __name__ == '__main__':
    unittest.main()