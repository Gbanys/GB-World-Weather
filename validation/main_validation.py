from datetime import datetime
from data_access.city_data.city_data import get_cities_in_json_format, get_city_latitude_and_longitude_coordinates

def check_if_graph_data_is_valid(city, startTime, endTime):

    try:
        get_city_latitude_and_longitude_coordinates(city)
    except KeyError:
        error_msg = "Please enter a valid city name"
        return error_msg
    
    if startTime is not None:
        try:
            startTime = datetime.strptime(startTime, "%Y-%m-%d")
        except ValueError:
            error_msg = "Please enter the start date in the correct format (YYYY-MM-dd)"
            return error_msg
            
    if endTime is not None:
        try:
           endTime = datetime.strptime(endTime, "%Y-%m-%d")
        except ValueError:
            error_msg = "Please enter the end date in the correct format (YYYY-MM-dd)"
            return error_msg
        
    if startTime is None and endTime is not None:
        error_msg = "Please specify the start date if you have specified the end date"
        return error_msg

    if (startTime is not None and endTime is not None) and (startTime > endTime):
        error_msg = "Dates are invalid, make sure that start date is earlier than end date"
        return error_msg
    
    return ""