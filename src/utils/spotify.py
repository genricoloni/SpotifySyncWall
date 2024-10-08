"""
Module for interacting with the Spotify API.
"""
import json

import requests
from spotipy import util


class SpotifyClient:
    """
    A class representing a client for interacting with the Spotify API.

    This client allows authentication and retrieval of the currently
    playing song for a specific user.

    Attributes:
        client_id (str): The client ID for Spotify API authentication.
        client_secret (str): The client secret for Spotify API authentication.
        username (str): The username associated with the Spotify account.
        scope (str): The access scope for the Spotify API.
        token (str): The authentication token for API requests.
        max_tries (int): The maximum number of attempts for API requests in case of failure.
        retry_delay (int): The delay between retries for API requests.
    """

    def __init__(self, client_id, client_secret, username):
        """
        Initialize a new instance of the SpotifyClient class.

        This method sets up the basic parameters required for authentication and
        calls the authenticate method to obtain the access token.

        Parameters:
            client_id (str): The client ID for Spotify API authentication.
            client_secret (str): The client secret for Spotify API authentication.
            username (str): The username associated with the Spotify account.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.scope = "user-read-currently-playing"
        self.token = None
        self.max_tries = 3
        self.retry_delay = 5
        self.authenticate()

    def authenticate(self):
        """
        Authenticate the client with the Spotify API.

        This method requests an authentication token using the provided client credentials
        and user information. It raises an exception if authentication fails.
        """
        self.token = util.prompt_for_user_token(self.username,
                                                self.scope,
                                                self.client_id,
                                                self.client_secret,
                                                redirect_uri="https://www.google.com/")

        if not self.token:
            raise requests.exceptions.RequestException("Authentication failed")

    def get_current_song(self):
        """
        Retrieve the currently playing song from Spotify.

        This method sends a request to the Spotify API to fetch the currently playing
        song for the authenticated user. It retries the request in case of errors
        up to `max_tries` times.

        Returns:
            dict: A dictionary containing song details, such as song title, artist name,
            album image URL, song ID, song length, and playing status. If no song is playing,
            or the request fails, it returns None.
        """
        header = {"Authorization": f"Bearer {self.token}"}
        url = "https://api.spotify.com/v1/me/player/currently-playing"

        for _ in range(self.max_tries):
            try:
                response = requests.get(url, headers=header, timeout=10)
                if response.status_code == 200:
                    content = json.loads(response.text)

                    status = content.get("is_playing")
                    item = content.get("item")
                    name = item.get("name")
                    artist_name = item.get("album").get("artists")[0].get("name")
                    image_url = item.get("album").get("images")[0].get("url")
                    song_id = item.get("id")
                    song_length = item.get("duration_ms")

                    data = {
                        "song_title": name,
                        "artist_name": artist_name,
                        "image_url": image_url,
                        "song_id": song_id,
                        "song_length": song_length,
                        "playing": status
                    }

                    # Check if all data values are valid
                    return data
            except requests.exceptions.RequestException as e:
                print(f"Error while getting current song: {e}")
                continue

        return None



    def get_audio_analysis(self, song_id):
        """SavedCo
        Get the audio analysis for a song from the Spotify API.

        Args:
            song_id (str): The ID of the song.

        Returns:
            dict or None: A dictionary with the audio analysis data, or None if the request fails.
        """


        url = f"https://api.spotify.com/v1/audio-analysis/{song_id}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()

        print("Error during request")
        return None
