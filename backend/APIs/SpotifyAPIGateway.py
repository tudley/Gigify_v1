import os
import base64
import json

from classes import Song, Artist
from dotenv import load_dotenv
from requests import post, get

load_dotenv()

class SpotifyAPIGateway():
    """
    A class modelling a gateway to the Spotify DB.
    Here, we can generate tokens, and query the Spotify DB for artists and their top songs
    """

    def __init__(self, client_id, client_secret, token=None, headers=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token
        self.headers = headers

    def get_token(self):
        """Here we are generating and returning our token to access the spotify web API
            Spotify required a base64 encoded string of "client_id:client_secret" """
        
        # here we build & encode the string 
        auth_string = self.client_id + ':' + self.client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        # declare the url we are going to interface with
        url = "https://accounts.spotify.com/api/token"

        # the headers and data attributes of the post request are defined here:
        headers = {
            "Authorization" : "Basic " + auth_base64,
            "Content-Type" : "application/x-www-form-urlencoded"
            }
        data = {"grant_type" : "client_credentials"}

        # lets upload our credentials to the spotify API to generate our token
        response = post(url, headers=headers, data=data)
        print(f"Spotify 'get_token' response: {response.status_code}")
        json_result = json.loads(response.content)
        token = json_result['access_token']
        
        return token
        
    def get_auth_header(self):
        """Once you have been authenticated, the header you want is different, as follows:"""
        return {"Authorization" : "Bearer " + self.token}

    def search_for_artist(self, artist):
        """Here we search for an artist by a string, returns Artist Object"""

        # Generate the headers for the request through the previous function
        self.headers = self.get_auth_header()

        # Build the query URL
        url = 'https://api.spotify.com/v1/search'
        query = f"q={artist}&type=artist&limit=1"
        query_url = url + '?' + query

        # Get the results through a get request
        response = get(query_url, headers=self.headers)
        print(f"Spotify db query status code: {response.status_code}")

        # Read the result
        json_result = json.loads(response.content)['artists']['items'][0]

        # If the search was unsuccessful:
        if len(json_result) == 0:
            print('no artists found...')
            return None
        
        # If the query 'name' value matches the string 'artist' argument, build artist object as verified
        if json_result['name'].lower().strip() == artist.lower().strip():
            artist = Artist(json_result['name'], json_result['id'], json_result['images'][0]['url'], verified = True)
        else:
            artist = Artist(json_result['name'], json_result['id'], json_result['images'][0]['url'])
        return artist
    
        
    def get_songs_by_artist(self, artist):
        """Find the top 10 songs in the UK of an artist from their ID previously found"""
        self.headers = self.get_auth_header()
        url = f"https://api.spotify.com/v1/artists/{artist.id}/top-tracks?country=UK"
        result = get(url, headers=self.headers)
        json_result = json.loads(result.content)['tracks']
        songs = []
        for entry in json_result:
            album_name = entry['album']['name']
            images = entry['album']['images']
            if images:
                album_cover = entry['album']['images'][0]['url']
            artist_name = artist.name
            album_id = entry['album']['uri']
            song_name = entry['name']
            song_id = entry['uri']

            song = Song(song_name, song_id, artist_name, album_name, album_id, album_cover)
            songs.append(song)
        return songs



if __name__ == "__main__":
    # OOP Approach
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    spotify = SpotifyAPIGateway(client_id, client_secret)
    spotify.token = spotify.get_token()
    artist = spotify.search_for_artist('The Prodigy')
    artist.catalog = spotify.get_songs_by_artist(artist)
    print(artist.to_dict())
