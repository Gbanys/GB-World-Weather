import json
import pandas as pd
from pathlib import Path

def get_cities_in_json_format() -> str:
    cities_data = pd.read_csv(f"{Path(__file__).parent.parent.absolute()}/worldcities.csv")
    cities, cities_lng, cities_lat = cities_data['city_ascii'].tolist(), cities_data['lng'].tolist(), cities_data['lat'].tolist()
    cities = json.dumps(cities)
    return cities, cities_lng, cities_lat

def get_city_latitude_and_longitude_coordinates(city: str):
    cities_data = pd.read_csv(f"{Path(__file__).parent.parent.absolute()}/worldcities.csv")
    cities_data = cities_data[cities_data['city_ascii'] == city].reset_index()
    latitude = cities_data.loc[0, 'lat']
    longitude = cities_data.loc[0, 'lng']
    return latitude, longitude