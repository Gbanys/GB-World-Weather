from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import uvicorn
from pathlib import Path
import requests
import json
import time
import pandas as pd
import plotly.graph_objects as go
from ip2geotools.databases.noncommercial import DbIpCity
from data_access.location_finder.location_finder import get_details_from_ip_address
from date_parser import parseFullMonth, parseHalfMonth
from weather_api import get_weather_types_for_date, get_weather_types_for_time, get_weather_type_for_each_row, get_weather_data_from_api
from data_access.city_data.city_data import get_cities_in_json_format, get_city_latitude_and_longitude_coordinates
from dash import Dash, dcc, html, Input, Output
from validation.main_validation import check_if_graph_data_is_valid
from plotting.plots import plot_weather_graph

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "GB-World-Weather" / "static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def return_home_page(request: Request):

    details_from_ip_address = get_details_from_ip_address()
    weather_data = get_weather_data_from_api(details_from_ip_address['Lat'], details_from_ip_address['Lng'], ['temperature_2m','windspeed_10m','relativehumidity_2m','pressure_msl','cloudcover','visibility', 'precipitation_probability'])

    weather_dataframe = pd.DataFrame(
        {'datetime': weather_data['hourly']['time'], 
         'temperature': weather_data['hourly']['temperature_2m'], 
         'precipitation_probability': weather_data['hourly']['precipitation_probability'],
         'cloudcover' : weather_data['hourly']['cloudcover'],
         }, 
         index=weather_data['hourly']['time']
    )

    weather_dataframe = weather_dataframe.assign(
        date=weather_dataframe.datetime.apply(lambda x: x.split("T")[0]), 
        time=weather_dataframe.datetime.apply(lambda x: x.split("T")[1]),
        weather_type=get_weather_types_for_time(weather_dataframe),
        day=weather_dataframe.datetime.apply(lambda x: x.split("T")[0].split("-")[2])
    )

    weather_types = get_weather_types_for_date(weather_dataframe)

    minimum_temperatures = weather_dataframe.groupby('date')['temperature'].min().tolist()
    maximum_temperatures = weather_dataframe.groupby('date')['temperature'].max().tolist()
    seven_day_forecast_dates = weather_dataframe.groupby('date')['temperature'].min().index.tolist()

    current_date = weather_data['current']['time'].split("T")[0]
    all_half_months = [parseHalfMonth(datetime.strftime(datetime.strptime(current_date, "%Y-%m-%d") + pd.Timedelta(f'{day} day'), "%Y-%m-%d")) for day in range(0, 7)]

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
    return templates.TemplateResponse("maps.html", context={'request' : request})

@app.get("/graphs")
async def return_graphs_page(request: Request):

    cities, cities_lng, cities_lat = get_cities_in_json_format()

    details_from_ip_address = get_details_from_ip_address()
    city = details_from_ip_address['Location'].split(",")[0]
    
    weather_data = get_weather_data_from_api(details_from_ip_address['Lat'], details_from_ip_address['Lng'], ['temperature_2m'])
    graph_url = plot_weather_graph(weather_data, 'temperature_2m', city)

    return templates.TemplateResponse("graphs.html", context={
        'request' : request,
        'cities' : cities,
        'error_msg' : '',
        'graph_url': graph_url,
        'zip' : zip
        }
    )

@app.post("/graphs")
async def handle_graph_data(
    request: Request,
    startTime: str = Form(None),
    endTime: str = Form(None),
    city: str = Form(...),
    metric_type: str = Form(...),
):
    
    cities, cities_lng, cities_lat = get_cities_in_json_format()
    
    error_msg = check_if_graph_data_is_valid(city, startTime, endTime)
    if error_msg != "":
        return templates.TemplateResponse("graphs.html", context={"request": request, "error_msg" : error_msg, "cities" : cities})

    city_latitude, city_longitude = get_city_latitude_and_longitude_coordinates(city)
        
    if startTime is not None and endTime is None:
        endTime = datetime.strftime(datetime.now(), "%Y-%m-%d")
    
    if startTime is not None and endTime is not None:
        startTime = datetime.strptime(startTime, "%Y-%m-%d")
        endTime = datetime.strptime(endTime, "%Y-%m-%d")

    weather_data = get_weather_data_from_api(city_latitude, city_longitude, [metric_type])

    graph_url = plot_weather_graph(weather_data, metric_type, city)
    
    return templates.TemplateResponse("graphs.html", context={
        'request' : request,
        'cities' : cities,
        'error_msg' : '',
        'graph_url' : graph_url,
        'zip' : zip
        }
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
