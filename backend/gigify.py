from flask import Flask, jsonify, request, redirect, render_template, url_for, redirect
from flask_cors import CORS
import os
import urllib.parse

from FlaskBackend.APIs.SpotifyAPIGateway import SpotifyAPIGateway
from FlaskBackend.APIs import TicketMasterAPIGateway
from FlaskBackend.APIs import ipinfoAPI
import FlaskBackend.APIs.APIIntergation as APIIntergation

app = Flask(__name__)
CORS(app)


# BASE ROUTES
@app.route("/") # homepage
def home():
    """Home url for the app"""
    return render_template('home.html')

@app.route('/playground') # homepage for accessing individual API services
def playground():
    """Menu for the playground feature"""
    return render_template('playground.html')



# INDIVIDUAL API HOMES
@app.route('/spotify_home') # query Spotify AIP here
def spotify_home():
    """Base for launching individual Spotify API queries"""
    return render_template('spotify_home.html')

@app.route('/ticketmaster_home') # Query Ticketmaster here
def ticketmaster_home():
    """Homepage for individual Ticketmaster queries"""
    return render_template('ticketmaster_home.html')

@app.route('/ipinfo') # query Ipinfo here
def ipinfo_home():
    return render_template('ipinfo_home.html')



# INDIVIDUAL API RESULT ROUTES - IpInfo, Spotify and Ticketmaster

@app.route('/get_location')
def get_location():
    ip = ipinfoAPI.find_ip()
    location = ipinfoAPI.find_ip_location(ip)
    context = location.to_dict()
    return render_template('ipinfo_show_location.html', context = context)

@app.route("/get_artist", methods=['POST']) # return Spotify API result
def get_artist():
    """Query the Spotify database for an artist, and return a JSON object of their details needed for web app"""
    
    # Build the gateway
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    spotify = SpotifyAPIGateway(client_id, client_secret)
    spotify.token = spotify.get_token()

    # Query Spotify
    artist_name = request.form['artist_name']
    artist = spotify.search_for_artist(artist_name)

    artist.catalog = spotify.get_songs_by_artist(artist) # returns full json
    artist_dict = artist.to_dict()
    return jsonify(artist_dict)

@app.route('/get_events', methods = ['POST']) # retuen Ticketmaster API result
def get_events_tm():
    print("Form data:", request.form)
    # instantiate API gateway
    ticketmaster = TicketMasterAPIGateway.TicketMasterAPIGateway() 
    # extract search params from request form
    city = request.form['city']
    radius = request.form['radius']
    unit = request.form['unit']
    # search db and return events
    ticketmaster.events = ticketmaster.get_events(lat=0, long=0, city=city, radius=radius, unit=unit)
    events = []
    for event in ticketmaster.events:
        events.append(event.to_dict())
    return render_template('ticketmaster_only_events.html', context=events)
    #return jsonify(events)

# MAIN API ROUTES
@app.route("/events/my_location_api")
def get_events_api():
    """MAIN METHOD OF GIGIFY, this url automatically generates all the information of local gigs, artists and their song IDs"""
    events = APIIntergation.get_events()
    return jsonify(events)

@app.route('/events/mylocation_web')
def get_events_web():    
    """As above, but returns result in html"""   
    events = APIIntergation.get_events()
    print(events)
    return render_template('get_events.html', events = events)





# SPOTIFY AUTH ROUTES
@app.route("/login")
def login():
    """Allow users to log into their Spotify account to allow app to access their user data"""
    client_id = os.getenv("SPOTIFY_CLIENT_ID") # get token info
    redirect_uri = "http://127.0.0.1:5000/callback" # where spotify redirects the user after Auth
    scopes = "playlist-modify-public playlist-modify-private" # permission parameters
    auth_url = (
        "https://accounts.spotify.com/authorize?"
        + urllib.parse.urlencode({
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": scopes
        }) 
    ) # this is effectively a post API, giving spotify data about who were authorizing, and what permissions we are allowing
    return redirect(auth_url)

@app.route("/callback")
def callback():
    """After """
    code = request.args.get("code") # exchange code for token
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)


