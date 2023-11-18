import requests
from ip2geotools.databases.noncommercial import DbIpCity
from typing import Any

def get_details_from_ip_address()-> dict[str, Any]:
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    res = DbIpCity.get(ip, api_key="free")
    details_from_ip_address = {"Location" : f'{res.city}, {res.region}, {res.country}', "Lat" : res.latitude, "Lng" : res.longitude}
    return details_from_ip_address