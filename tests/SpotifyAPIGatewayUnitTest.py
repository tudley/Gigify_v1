import unittest
from unittest.mock import patch, Mock
#import dotenv
#import os
from gigify.APIs.SpotifyAPIGateway import SpotifyAPIGateway
from gigify.APIS.classes import Artist, Song

#.load_dotenv()

class SpotifyGatewayTest(unittest.TestCase):

    def setUp(self):
        self.clientId = 'fakeId'
        self.clientSecret = 'fakeSecret'
        self.spotify = SpotifyAPIGateway(self.clientId, self.clientSecret)
    
    @patch('spotify_gateway.post')
    def testGetTokenSuccess(self, mock_post):
        """Compare the get_token method agsint a proven"""
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"access_token" : "mock_token"}'
        mock_post.return_value = mock_response

        token = self.spotify.get_token()
        self.assertEqual(token, "mock_token")
        mock_post.assert_called_once()
        

    def testGetTokenInvalid():

        # client id/secret valid
        pass

    def test_get_auth_header():
        pass

    def search_for_artist():
        # no artist found

        # exact match found

        # spotify autocorrects search string
        
        pass

    def get_songs_by_artist():
        pass
