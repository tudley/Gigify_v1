class Location():
    """A class modelling a location in the world"""
    def __init__(self, name, long, lat):
        self.name = name
        self.long = long
        self.lat = lat

    def to_dict(self):
        """Returns object in jsonify-able format"""
        return {
            'name' : self.name,
            'long' : self.long,
            'lat' : self.lat,
        }
    

class Song():
    """A class modelling a song, with links to Spotifys' database"""
    def __init__(self, song_name, song_id, artist, album_name, album_id, album_cover):
        self.song_name = song_name
        self.song_id = song_id
        self.artist = artist
        self.album_name = album_name
        self.album_id = album_id
        self.album_cover = album_cover

    def to_dict(self):
        """Returns object in jsonify-able format"""
        return {
            'song name' : self.song_name,
            'song id' : self.song_id,
            'artist' : self.artist,
            'album name' : self.album_name,
            'album id' : self.album_id,
            'album cover' : self.album_cover
        }



class Artist():
    """A class modelling an artist with a link to Spotifys' DB"""
    def __init__(self, name, id, picture, verified = False):
        self.name = name
        self.id = id
        self.verified = verified
        self.picture = picture
        self.catalog = []

    def to_dict(self):
        """Returns object in jsonify-able format"""
        return {
            "name": self.name,
            "id": self.id,
            "verified": self.verified,
            "picture" : self.picture,
            "catalog" : [song.to_dict() for song in self.catalog]

        }
    
class Venue():
    """Class representing a venue, where an Event is held"""
    def __init__(self, name, id, long, lat, address):
        self.venue_name = name
        self.venue_id = id
        self.long = long
        self.lat = lat
        self.address = address

    def to_dict(self):
        """Returns object in jsonify-able format"""
        return {
        'venue name' : self.venue_name,
        'venue id' : self.venue_id,
        'long' : self.long, 
        'lat' : self.lat,
        'address' : self.address 
        }


class Event():
    """Class representing an event, where an Artist performs"""
    def __init__(self, name, venue, date):
        self.event_name = name
        self.artist = None
        self.artist_name = None
        self.venue = venue
        self.date = date

    def to_dict(self):
        """Returns object in jsonify-able format"""
        if self.artist != None:
            # self.artist is an Artist, can ,to_dict()
            return {
                "event name": self.event_name,
                "artist": self.artist.to_dict(),
                "venue": self.venue.to_dict(),
                "date" : self.date,
            }
        else:
            return{
                #self.artist == None, no to_dict() method
                "event name": self.event_name,
                "artist name": self.artist_name,
                "venue": self.venue.to_dict(),
                "date" : self.date,
            }