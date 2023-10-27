import requests
from dotenv import dotenv_values
import os
from geopy.distance import geodesic
from pydantic import validate_call

dotenv_path = os.getenv("DOTENV_PATH", ".env")
config = dotenv_values(dotenv_path)

@validate_call
def get_route(domicile_lat: float, domicile_lng: float, travail_lat: float, 
              travail_lng: float, time_spent: float):

    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    destination = f"{travail_lat}, {travail_lng}"
    origins = f"{domicile_lat}, {domicile_lng}"
    # Construisez le corps de la requête
    params = {
        'destinations': destination,
        'origins': origins,
        'key': config["YOUR_API_KEY"]
    }

    response = requests.get(base_url, params=params)
    response = response.json()

    return compute_total_distance_and_time(response, domicile_lat , domicile_lng ,
                                           travail_lat, travail_lng, time_spent)

@validate_call
def compute_total_distance_and_time(response: dict, domicile_lat: float, domicile_lng: float,
                                    travail_lat: float, travail_lng: float, time_spent: float):
    total_distance = 0  # en mètres
    total_time = 0      # en secondes
    distance_daily = None
    time_daily = None

    # Vérifiez si les données sont valides
    if response.get("status") == "OK":
        data = response.get("rows")
        for element in data[0]["elements"]:
            total_distance += element["distance"]["value"]
            total_time += element["duration"]["value"]
        time_daily = total_time
        distance_daily = total_distance
        distance_daily *= 2/1000
        time_daily *= 2

        return distance_daily, time_daily
    else:
        distance_daily = geodesic((domicile_lat,domicile_lng), (travail_lat,travail_lng)).kilometers
        distance_daily *= 2
        time_daily = time_spent*2
        return distance_daily, time_daily
