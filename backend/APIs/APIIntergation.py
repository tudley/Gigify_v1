from FlaskBackend.APIs import SpotifyAPIGateway
from FlaskBackend.APIs import ipinfoAPI
from FlaskBackend.APIs import TicketMasterAPIGateway
import os

#   Process for get_events()
# 1. Use IPInfoAPI to determine users loction

# 2. Use TicketMasterAPI to find events near users location

# 2.5 OPTIONAL: Either use TicketMaster 'ClassificationName' param to specify genre, or use SpotifyAPI to filter artists based on user reccomendations

# 3. Query Spotify API using events name as our search.
# an artist object is build as specced in SpotifyAPIGateway

# 4.   Process for create_playlist()
#   a. Spotify links to users account
#   b. Spotify finds top 5 songs by each artist
#   c. Spotify creates playlist


def get_events():

    # 1. locate users location
    ip = ipinfoAPI.find_ip()
    location = ipinfoAPI.find_ip_location(ip)
    
    # 2. find events
    ticketmaster = TicketMasterAPIGateway.TicketMasterAPIGateway()
    ticketmaster.events = ticketmaster.get_events(location.lat, location.long,) #city='Bristol')

    # 3. build artist objects 
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    spotify = SpotifyAPIGateway.SpotifyAPIGateway(client_id, client_secret)
    spotify.token = spotify.get_token()

    db = []
    for event in ticketmaster.events:

        artist_name = event.event_name
        artist = spotify.search_for_artist(artist_name)
        event.artist = artist
        artist.catalog = spotify.get_songs_by_artist(artist)
        artist_dict = artist.to_dict()
        #print(f"The event is called {event.event_name}, where {event.artist.name} is playing at {event.venue.venue_name} on {event.date}.")
        #print(f"Here is some of their top songs:")
        #for song in artist.catalog[:2]:
        #    print(song)

        db.append(event.to_dict())

    return(db) 

    # 4. Verify and filter artists

    # 5. Create user playlist





if __name__ == '__main__':      
    db = get_events()
    print(db)

    for event in db:
        print(f"{event['event name']} : {event['artist']['name']},")
