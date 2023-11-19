import plotly.graph_objects as go
import os
from datetime import datetime
from glob import glob

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
    graph_url = f"../static/img/weather_graph{time_now}.png"

    weather_graph_directories = glob("../static/img/weather_graph*")

    if weather_graph_directories:
        for dir in weather_graph_directories:
            os.remove(dir)

    fig.write_image(graph_url)

    return graph_url