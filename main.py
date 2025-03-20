import json
import os
import spotipy
import lyricsgenius as lg

from env import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, GENIUS_ACCESS_TOKEN

scope = "user-read-currently-playing"

oauth = spotipy.oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope)
token_dict = oauth.get_access_token()
token = token_dict['access_token']

spotify = spotipy.Spotify(auth=token)

genius = lg.Genius(GENIUS_ACCESS_TOKEN)

current_song = spotify.current_user_playing_track()
artist = current_song['item']['artists'][0]['name']
song_name = current_song['item']['name']
popularity = current_song['item']['popularity']

print(artist, "–", song_name, "(" + str(popularity) + "%)")

genius_song = genius.search_song(song_name, artist)
print(genius_song.lyrics)