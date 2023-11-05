import pandas as pd

def get_weather_type_for_each_row(row):
        if row['cloudcover'] > 90 and row['precipitation_probability'] > 75:
            return "heavy rain"
        elif row['cloudcover'] > 90 and row['precipitation_probability'] > 50:
            return "rain"
        elif row['cloudcover'] > 50 and row['precipitation_probability'] > 50:
            return "cloudy with rain"
        elif row['cloudcover'] > 90 and row['precipitation_probability'] < 50:
            return "overcast"
        elif row['cloudcover'] < 20:
            return "sunny"
        elif row['cloudcover'] > 50 and row['precipitation_probability'] < 50:
            return "cloudy"
        else:
            return "cloudy"


def get_weather_types_for_date(weather_dataframe: pd.DataFrame):
    cloudcover = weather_dataframe.groupby('date')['cloudcover'].mean()
    precipitation_probability = weather_dataframe.groupby('date')['precipitation_probability'].mean()
    grouped_dataframe = pd.DataFrame({'cloudcover' : cloudcover, 'precipitation_probability': precipitation_probability}, index=cloudcover.index.tolist())

    grouped_dataframe['weather_type'] = grouped_dataframe.apply(get_weather_type_for_each_row, axis=1)
    return grouped_dataframe['weather_type']

def get_weather_types_for_time(weather_dataframe: pd.DataFrame):
    return weather_dataframe.apply(get_weather_type_for_each_row, axis=1)
