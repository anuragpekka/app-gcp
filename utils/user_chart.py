from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from opencage.geocoder import OpenCageGeocode
from  .astro_details import AstroDetails
import os

# Load environment variables
load_dotenv()
OPENCAGE_API_KEY = os.environ.get("OPENCAGE_API_KEY")


def find_lat_long_geopy(place: str):
    print(">>> In find_lat_long_geopy")
    # Initialize geolocator
    geolocator = Nominatim(user_agent="geoapi")

    # Get location
    location = geolocator.geocode(place)
    if not location:
            return None, None
    return location.latitude, location.longitude


def find_lat_lon_opencage(place_name: str):
    print(">>> In find_lat_lon_opencage")
    geocoder = OpenCageGeocode(OPENCAGE_API_KEY)
    result = geocoder.geocode(place_name)
    if not result:
        return None, None
    return result[0]["geometry"]["lat"], result[0]["geometry"]["lng"]


def find_lat_lon(place):
     try:
        lat, lon = find_lat_long_geopy(place)
        if((lat == None ) and (lon == None)):
            lat, lon = find_lat_lon_opencage(place)
            print(">>> latitude, longitude not found in first attempt")
        return lat, lon
     except Exception as e:
        print(e)
        print(">>> Error in finding latitude and longitude. Trying again...")
        lat, lon = find_lat_lon_opencage(place)
        return lat, lon


def full_birth_chart_details(year,month,day,hour,minute,second,place):
    latitude, longitude = find_lat_lon(place)
    # latitude, longitude = 23.3441, 85.3096 #testing
    ad = AstroDetails(year = year, month = month, day = day,
                      hour = hour, minute = minute, second = second,
                      lat = latitude, lon = longitude)
    astro_details_json = ad.astrology_chart_details()
    return astro_details_json
