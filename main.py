import requests
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
import pandas as pd
import argparse
import os

load_dotenv()
API_KEY = os.environ['API_KEY']
API_ENDPOINT = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"


def getLatitudeAndLongitude(city):
    geolocator = Nominatim(user_agent="RestaurantParser")
    location = geolocator.geocode(city)
    if location:
        return str(location.latitude) + "," + str(location.longitude)
    return ""


def exportJsonToExcelSheet(jsonData, sheetName):
    df = pd.DataFrame(jsonData)
    df.to_excel(sheetName + ".xlsx", index=False)


def main():
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('city_arg', type=str, help='A required city name to find restaurants for')
    parser.add_argument('sheet_arg', type=str,
                        help='A required argument for your excel sheet name')
    parser.add_argument('radius_arg', type=int, nargs='?',
                        help='An optional argument for radius for number of restaurants')
    args = parser.parse_args()
    params = {
        "location": getLatitudeAndLongitude(args.city_arg),
        "radius": args.radius_arg if args.radius_arg else 2000,
        "type": "restaurant",
        "key": API_KEY,
    }

    response = requests.get(API_ENDPOINT, params=params)

    if response.status_code == 200:
        exportJsonToExcelSheet(jsonData=response.json()["results"], sheetName=args.sheet_arg)
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    main()