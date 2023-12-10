import pandas as pd
import requests
from names.weather_event_names import day_weather_event_names, night_weather_event_names
from names.european_city_names import EUROPEAN_CITIES
import numpy as np
from pathlib import Path

def get_weather_type_for_each_row(row) -> str:

    if type(row['weather_code']) == np.ndarray:
        row['weather_code'] = row['weather_code'][0]

    if row['is_day'] == 1:
        return day_weather_event_names[str(row['weather_code'])]
    else:
        return night_weather_event_names[str(row['weather_code'])]


def get_weather_types_for_date(weather_dataframe: pd.DataFrame, average_weather_type: bool) -> pd.Series:
    weather_code = weather_dataframe.groupby('date')['weather_code'].apply(lambda x: np.array(x.mode()))
    is_day = weather_dataframe.groupby('date')['is_day'].apply(lambda x: np.array(x.mode()))
    grouped_dataframe = pd.DataFrame({'weather_code' : weather_code, 'is_day' : is_day}, index=weather_code.index.tolist())

    if average_weather_type:
        grouped_dataframe = grouped_dataframe.assign(is_day=1)

    grouped_dataframe['weather_type'] = grouped_dataframe.apply(get_weather_type_for_each_row, axis=1)
    return grouped_dataframe['weather_type']


def get_weather_types_for_time(weather_dataframe: pd.DataFrame) -> pd.Series:
    return weather_dataframe.apply(get_weather_type_for_each_row, axis=1)


def get_weather_data_from_api(latitude: float, longitude: float, metrics: list[str]):
    metrics_in_url = ",".join(metrics)
    weather_request = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current={metrics_in_url}&hourly={metrics_in_url}")
    weather_data = weather_request.json()
    return weather_data


def get_current_weather_from_european_cities(metrics: list[str]) -> dict:
    european_cities = EUROPEAN_CITIES
    all_cities = pd.read_csv(f"{Path(__file__).parent.parent.absolute()}/worldcities.csv")
    european_cities_only = all_cities[all_cities['city_ascii'].isin(european_cities)].drop_duplicates(subset=['city_ascii'])

    european_weather = {}
    for city, latitude, longitude in zip(european_cities_only['city_ascii'], european_cities_only['lat'], european_cities_only['lng']):
        current_weather = get_weather_data_from_api(latitude, longitude, metrics)
        european_weather[city] = current_weather['current']
        european_weather[city]['lat'] = latitude
        european_weather[city]['long'] = longitude
        european_weather[city]['max_temperature'] = max(current_weather['hourly']['temperature_2m'][:24])
        european_weather[city]['min_temperature'] = min(current_weather['hourly']['temperature_2m'][:24])
        european_weather[city]['precipitation_probability'] = round(np.mean(current_weather['hourly']['precipitation_probability'][:24]), 1)
        european_weather[city]['humidity'] = round(np.mean(current_weather['hourly']['relative_humidity_2m'][:24]), 1)
        european_weather[city]['cloudiness'] = round(np.mean(current_weather['hourly']['cloudcover'][:24]), 1)

    return european_weather

    



