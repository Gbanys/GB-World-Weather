from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import uvicorn
from pathlib import Path
import requests
import pandas as pd
from ip2geotools.databases.noncommercial import DbIpCity
from date_parser import parseFullMonth, parseHalfMonth
from weather_api import get_weather_types_for_date, get_weather_types_for_time, get_weather_type_for_each_row

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "GB-World-Weather" / "static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def return_home_page(request: Request):

    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    res = DbIpCity.get(ip, api_key="free")
    details_from_ip_address = {"Location" : f'{res.city}, {res.region}, {res.country}', "Lat" : res.latitude, "Lng" : res.longitude}
    weather_request = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={details_from_ip_address['Lat']}&longitude={details_from_ip_address['Lng']}&current=temperature_2m,windspeed_10m,relativehumidity_2m,pressure_msl\
,cloudcover,visibility,precipitation_probability&hourly=temperature_2m,relativehumidity_2m,windspeed_10m,precipitation_probability,cloudcover")
    weather_data = weather_request.json()
    weather_data['current']

    weather_dataframe = pd.DataFrame(
        {'datetime': weather_data['hourly']['time'], 
         'temperature': weather_data['hourly']['temperature_2m'], 
         'precipitation_probability': weather_data['hourly']['precipitation_probability'],
         'cloudcover' : weather_data['hourly']['cloudcover'],
         }, 
         index=weather_data['hourly']['time']
    )

    weather_dataframe['date'] = weather_dataframe.datetime.apply(lambda x: x.split("T")[0])
    weather_dataframe['time'] = weather_dataframe.datetime.apply(lambda x: x.split("T")[1])
    weather_dataframe['weather_type'] = get_weather_types_for_time(weather_dataframe)

    weather_types = get_weather_types_for_date(weather_dataframe)

    minimum_temperatures = weather_dataframe.groupby('date')['temperature'].min().tolist()
    maximum_temperatures = weather_dataframe.groupby('date')['temperature'].max().tolist()
    seven_day_forecast_dates = weather_dataframe.groupby('date')['temperature'].min().index.tolist()

    current_date = weather_data['current']['time'].split("T")[0]
    all_half_months = [parseHalfMonth(datetime.strftime(datetime.strptime(current_date, "%Y-%m-%d") + pd.Timedelta(f'{day} day'), "%Y-%m-%d")) for day in range(0, 7)]

    weather_dataframe['day'] = weather_dataframe['date'].apply(lambda x: x.split("-")[2])
    seven_day_forecast_weather_details = [weather_dataframe.groupby("day")[metric].apply(list).to_dict() for metric in ['time', 'weather_type', 'temperature', 'precipitation_probability']]

    return templates.TemplateResponse(
        "home.html", 
        context={
            "request": request, 
            "current_location": details_from_ip_address['Location'],
            "full_month" : parseFullMonth(current_date),
            "time": weather_data['current']['time'].split("T")[1],
            "temperature": weather_data['current']['temperature_2m'],
            "cloudiness": weather_data['current']['cloudcover'],
            "pressure": weather_data['current']['pressure_msl'],
            "humidity": weather_data['current']['relativehumidity_2m'],
            "visibility": weather_data['current']['visibility'],
            "windspeed" : weather_data['current']['windspeed_10m'],
            "current_weather_type": get_weather_type_for_each_row(weather_data['current']),
            "weather_modal_box_id" : range(1, 8),
            "forecast_info" : zip(minimum_temperatures, maximum_temperatures, all_half_months, weather_types, range(1, 8)),
            "seven_day_forecast_dates" : seven_day_forecast_dates,
            "seven_day_forecast_full_dates" : [parseFullMonth(seven_day_forecast_dates[date_index]) if date_index != 0 else "today" for date_index in range(0, len(seven_day_forecast_dates))],
            "seven_day_forecast_details_time" : [value for value in seven_day_forecast_weather_details[0].values()],
            "seven_day_forecast_details_weather_type" : [value for value in seven_day_forecast_weather_details[1].values()],
            "seven_day_forecast_details_temperature" : [value for value in seven_day_forecast_weather_details[2].values()],
            "seven_day_forecast_details_precipitation" : [value for value in seven_day_forecast_weather_details[3].values()],
            "zip":zip
            }
    )

@app.get("/maps")
async def return_maps_page(request: Request):
    print("Hello")
    return templates.TemplateResponse("maps.html", context={'request' : request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
