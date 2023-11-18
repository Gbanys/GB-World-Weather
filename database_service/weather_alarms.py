from db_connect import connect_to_amazon_rds
from data_access.city_data.city_data import get_city_latitude_and_longitude_coordinates
from weather_api import get_weather_data_from_api
from weather_event_names import day_weather_event_names, night_weather_event_names
import pandas as pd
from datetime import datetime

def retrieve_subscriber_information() -> pd.DataFrame:

    connection = connect_to_amazon_rds()
    mycursor = connection.cursor()

    subscriber_dataframe = pd.read_sql("SELECT * FROM alarms;", connection)

    return subscriber_dataframe


def retrieve_required_messages_and_phone_numbers(subscriber_dataframe: pd.DataFrame, weather_api):

    phone_number_dictionary = {}

    for _, subscriber in subscriber_dataframe.iterrows():

        city_latitude, city_longitude = get_city_latitude_and_longitude_coordinates(subscriber['city'])
        weather_data = weather_api.get_weather_data_from_api(city_latitude, city_longitude, ['temperature_2m', 'precipitation_probability', 'wind_speed_10m'])
        weather_event, notify_before, phone_number = subscriber['weather_event'], subscriber['notify_before'], subscriber['phone_number']

        weather_dataframe = pd.DataFrame(
            {
                'weather_type' : weather_data['hourly']['weather_code'],
                'is_day' : weather_data['hourly']['is_day'],
                'temperature_2m' : weather_data['hourly']['temperature_2m'],
                'precipitation_probability' : weather_data['hourly']['precipitation_probability'],
                'wind_speed_10m' : weather_data['hourly']['wind_speed_10m'],
            },
            index=pd.to_datetime(weather_data['hourly']['time'])
        )
        weather_dataframe['weather_type'] = weather_dataframe.apply(lambda row: day_weather_event_names[str(int(row['weather_type']))] if row['is_day'] == 1 else night_weather_event_names[str(int(row['weather_type']))], axis=1)

        if weather_event is not None:
            weather_events = weather_dataframe.loc[pd.to_datetime(weather_data['current']['time']) : pd.to_datetime(weather_data['current']['time']) + pd.Timedelta(hours=notify_before), 'weather_type']
            first_event_occurence = weather_events[weather_events == weather_event].index[0]
            message = f"Hello. This is a notification from world weather forecast. {weather_event} weather is expected on {str(first_event_occurence)}"
            phone_number_dictionary[phone_number] = {}
            phone_number_dictionary[phone_number]['new_weather_event'] = message

        if subscriber['metric_limit'] is not None:
            metrics = weather_dataframe.loc[pd.to_datetime(weather_data['current']['time']) : pd.to_datetime(weather_data['current']['time']) + pd.Timedelta(hours=notify_before), subscriber['metric']]
            first_event_occurence = metrics[metrics > subscriber['metric_limit']].index[0]
            exceeded_metric = metrics[metrics > subscriber['metric_limit']].iloc[0]
            message = f"Hello. This is a notification from world weather forecast. Your selected {subscriber['metric']}\
                  will be exceeded on {str(first_event_occurence)}. {subscriber['metric']} will be {str(exceeded_metric)} at this time"
            phone_number_dictionary[phone_number] = {}
            phone_number_dictionary[phone_number]['exceeded_metric'] = message

    return phone_number_dictionary
            



