import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os
from datetime import datetime
from glob import glob
from mpl_toolkits.basemap import Basemap
from pathlib import Path

def plot_weather_graph(weather_data: dict, metric_type: str, city: str) -> str:

    COLORS = {"temperature_2m" : "red", "cloud_cover" : "green", "wind_speed_10m" : "cyan", "precipitation" : "blue"}
    
    fig = go.Figure([go.Scatter(x=weather_data['hourly']['time'], y=weather_data['hourly'][metric_type], line=dict(color=COLORS[metric_type]))])
    fig.update_layout(
        plot_bgcolor="rgb(10, 10, 10)",
        paper_bgcolor = "rgb(10, 10, 10)",
        title_text = f'{metric_type} graph for {city}',
        title_font_color = COLORS[metric_type],
        font_color = "white",
    )
    
    time_now = datetime.strftime(datetime.now(), "%Y-%m-%d")
    graph_url = f"{Path(__file__).parent.parent.absolute()}/static/img/weather_graph{time_now}.png"

    weather_graph_directories = glob("../static/img/weather_graph*")

    if weather_graph_directories:
        for dir in weather_graph_directories:
            os.remove(dir)

    fig.write_image(graph_url)
    graph_url = f"static/img/weather_graph{time_now}.png"

    return graph_url


def plot_europe_temperature_map(european_weather: dict):

    map = Basemap(projection='mill', llcrnrlat=30, urcrnrlat=70, llcrnrlon=-25, urcrnrlon=40)
    fig = plt.figure(figsize = (20,7), dpi=200)

    map.drawcoastlines()
    map.fillcontinents(color='green', lake_color='darkblue')
    map.drawmapboundary(fill_color='darkblue')
    map.drawcountries()

    for weather_dict in european_weather.values():
        if weather_dict["temperature_2m"] < 4:
            temp_box_color = 'cyan'
        elif weather_dict["temperature_2m"] < 11:
            temp_box_color = 'lime'
        elif weather_dict["temperature_2m"] < 19:
            temp_box_color = 'yellow'
        elif weather_dict["temperature_2m"] < 26:
            temp_box_color = 'orange'
        else:
            temp_box_color = 'red'
            
        x_coord, y_coord = map(weather_dict['long'], weather_dict['lat'])
        plt.annotate(f'{weather_dict["temperature_2m"]}°C', xy=(x_coord, y_coord), xytext=(0, 0), 
                textcoords='offset points', ha='center', va='bottom',color='black',
                bbox=dict(boxstyle='round,pad=0.2', fc=temp_box_color))
    
    time_now = datetime.strftime(datetime.now(), "%Y-%m-%d")
    map_url = f"{Path(__file__).parent.parent.absolute()}/static/img/european_map{time_now}.png"

    weather_graph_directories = glob("../static/img/european_map*")

    if weather_graph_directories:
        for dir in weather_graph_directories:
            os.remove(dir)

    fig.savefig(map_url, bbox_inches='tight')
    map_url = f"static/img/european_map{time_now}.png"

    return map_url