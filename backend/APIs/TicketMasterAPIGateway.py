import requests
import json
import dotenv
import os
from classes import Venue, Event

dotenv.load_dotenv()



class TicketMasterAPIGateway():
    """Class modelling a gateway to TicketMaster API, where queries on events are made"""
    
    def __init__(self):
        self.consumer_key = os.getenv('TicketMaster_consumer_key')
        self.url = 'https://app.ticketmaster.com/discovery/v2/events.json'
        self.events = []
        self.venues = []
        self.size = 10
        self.radius = 15
        self.unit = 'miles'
        self.cities = [] # A list to hold all possible cities Ticketmaster offer as a query
        self.params = {
            'apikey' : self.consumer_key,
            'classificationName' : 'music',
            'size' : self.size,
            'radius' : self.radius,
            'unit' : self.unit
        }
        self.events_dict = None
        
    def get_cities(self):
        """PLEASE FLESH THIS OUT
            function which find what cities TM has in its db...
        """
        temp_params ={
            'apikey' : self.consumer_key,
            'classificationName' : 'music',
            'countryCode' : 'GB'
        }
        response = requests.get(self.url, params=temp_params)
        response_json = response.json()
        print(response.status_code)
        events = response_json['_embedded']['events']
        cities = []
        for event in events:
            city = event['_embedded']['venues'][0]['city']['name']
            print(city)
            if city not in cities:
                cities.append(city)
        cities = sorted(cities)
        return cities


    def update_params_latlong(self, lat, long , radius=20, unit='miles', size=10):
        """Adjust the search parameters to only 'latlong'"""
        self.params['radius'] = radius
        self.params['unit'] = unit
        self.params['size'] = size
        if lat and long:
            self.params['city'] = None
            self.params['latlong'] = f"{lat},{long}"

    def update_params_city(self, city,radius=20, unit='miles', size=10):
        """Adjust the search parameters to only 'city'"""
        self.params['radius'] = radius
        self.params['unit'] = unit
        self.size = size
        if city:
            self.params['city'] = city
            self.params['latlong'] = None

    def check_new_venue(self, venue_name):
        """Check if Venue object already exists in memory"""
        for venue in self.venues:
            if venue_name == venue.venue_name:
                return venue
        return False
    
    def parse_response(self, events):
        """Parse results of API call response to """
        list_of_event_objects = []
        for event_data in events['_embedded']['events']:
            #print(event_data['_embedded']['venues'][0])
        #print(f"{event['name']} playing at {event['_embedded']['venues'][0]['name']}" + 
            #f"on {event['dates']['start']['dateTime']}")

            # event details
            event_name = event_data['name']
            event_artist_name = event_data['_embedded']['attractions'][0]['name']
            event_time = event_data['dates']['start']['dateTime']

            # venue details
            venue_data = event_data['_embedded']['venues'][0]

            venue_name = venue_data.get('name', 'unknown')
            venue_id = venue_data.get('id', 'unknown')
            venue_location = venue_data.get('location')
            if venue_location:
                venue_long = venue_location['longitude']
                venue_lat = venue_location['latitude']
            venue_address = venue_data.get('address')

            # create new venue if no venue exists with matching values
            venue = self.check_new_venue(venue_name)
            if not venue:
                venue = Venue(venue_name, venue_id, venue_long, venue_lat, venue_address)
                self.venues.append(venue)
            event_obj =Event(event_name, venue, event_time)
            list_of_event_objects.append(event_obj)
        return list_of_event_objects
            

    def get_events(self, lat, long, city=None, radius=15, unit='miles'):
        """Return a List of Event objects based on events happening local
            to the user within a month from now"""
        
        # if user provides a city, use that, otherwise use default of users IP LatLong
        if city:
            self.update_params_city(city, radius, unit)
        else:
            self.update_params_latlong(lat, long, radius, unit)

        response = requests.get(self.url, params=self.params)
        print(f"developer.ticketmaster.com API status: {response.status_code}")

        # If the request was successful, filter the artist names out of the response, and add it to an empty list
        if response.status_code == 200:
            events = response.json()
            list_of_event_objects = self.parse_response(events)
            return list_of_event_objects
        
        # if request fails, return an empty list
        else:
            print('request failed')
            return []


if __name__ == '__main__':
    ticketmaster = TicketMasterAPIGateway()
    lat, long = 51.5407,-2.4184

    if True:
        # default query, no city info used
        ticketmaster.events = ticketmaster.get_events(lat, long)
        for event in ticketmaster.events:
            print(f"{event.event_name}: watch {event.artist_name} playing at {event.venue.venue_name} on {event.date}")

    if False:
        # query where user manually inputs city:
        ticketmaster.events = ticketmaster.get_events(lat, long, 'Brighton')
        for event in ticketmaster.events:
            print(f"{event.event_name}: watch {event.artist_name} playing at {event.venue.venue_name} on {event.date}")

    if False:
        # test get_city() functionality
        cities = ticketmaster.get_cities()
        #print(cities['_embedded']['events'][0]['_embedded']['venues'][0]['city']['name'])
        print(cities)
        