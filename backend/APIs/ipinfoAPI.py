from classes import Location

import requests
import dotenv
import os

dotenv.load_dotenv()

def find_ip():
    response = requests.get('https://api.ipify.org')
    ip = response.text
    print(f"api.ipify.org API status: {response.status_code}")
    return ip

def find_ip_location(ip):
    """Find the Users location to the nearest city"""
    # Initiallise variables for the API call
    token = os.getenv('IPInfoAPI_token')
    url = f"https://ipinfo.io/{ip}?token={token}"
    # Get a response object and filter through its JSON to extract it's 'city' value
    response = requests.get(url)
    print(f"ipinfo.io API status: {response.status_code}")
    data = response.json()
    lat_str, long_str = data['loc'].split(",")
    lat = float(lat_str)
    long = float(long_str)
    name = data['city']
    location = Location(name, long, lat)
    return location

def findUserLocation():
    """Demo of method to return location of users current IP"""
    ip = find_ip()
    location = find_ip_location(ip)
    return location

if __name__ == '__main__':
    location = findUserLocation()
    print(location.long, location.lat)


    

