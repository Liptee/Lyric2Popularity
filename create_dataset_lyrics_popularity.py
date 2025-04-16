import spotipy
import lyricsgenius as lg
import json
import os
from time import sleep

from env import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, GENIUS_ACCESS_TOKEN


sleep_time = 0
N = 20
quaries = ["United Albums", 
           "Radiohead", 
           "Beatles", 
           "Rolling Stones",
           "Queen",
           "Coldplay",
           "Eminem",
           "Taylor Swift",
           "Adele",
           "Ed Sheeran",
           "Kendrick Lamar",
           "Drake",
           "Post Malone",
           "Travis Scott",
           "Billie Eilish",
           "Ariana Grande",
           "The Smiths",
           "Muse",
           "Cyberpunk",
           "Matrix",
           "Dad rock",
           "Grunge",
           "Britpop",
           "Nu-metal",
           "Hip-hop",
           "Rap",
           "Country",
           "Blues",
           "Jazz",
           "Funk",
           "Soul",
           "R&B",
           "Russian",
           "USA",
           "UK",
           "France",
           "Germany",
           "Italy",
           "Spain",
           "Portugal",
           "Argentina",
           "Brazil",
           "Latino",
           "Japan",
           "Korea",
           "China",
           "Australia",
           "New Zealand",
           "Ukraine",
           "Poland",
           "Czech Republic",
           "Slovakia",
           "Hungary",
           "Romania",
           "Bulgaria"
           ]

tracks_path = "tracks/with_lyrics"
files_with_lyrics = os.listdir(tracks_path)
ids_with_lyrics = [file.split(".")[0] for file in files_with_lyrics]

tracks_path = "tracks/no_lyrics"
files_no_lyrics = os.listdir(tracks_path)
ids_no_lyrics = [file.split(".")[0] for file in files_no_lyrics]

ids = ids_with_lyrics + ids_no_lyrics

scope = "playlist-modify-public"

auth = spotipy.oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope)
token_dict = auth.get_access_token()
token = token_dict['access_token']
sp = spotipy.Spotify(auth=token)

genius = lg.Genius(GENIUS_ACCESS_TOKEN)

for QUERY in quaries:
    results = sp.search(q=QUERY, type="playlist", limit=N)
    playlists = results.get("playlists", {}).get("items", [])

    for playlist in playlists:
        try:
            print("Spotify API:")
            playlist_id = playlist["id"]
            playlist_name = playlist["name"]
            tracks_data = sp.playlist_tracks(playlist_id)
            tracks = tracks_data.get('items', [])
            for track in tracks:
                sleep(sleep_time)
                try:
                    available_markets = track["track"]["available_markets"]
                    explicit = track["track"]["explicit"]
                    track_id = track["track"]["id"]
                    release_date = track["track"]["album"]["release_date"]
                    track_artist = track["track"]["artists"][0]["name"]
                    artist_id = track["track"]["artists"][0]["id"]
                    track_name = track["track"]["name"]
                    album_name = track["track"]["album"]["name"]
                    album_id = track["track"]["album"]["id"]
                    duration_ms = track["track"]["duration_ms"]
                    popularity = track["track"]["popularity"]
                except Exception as e:
                    print("Error getting track info")
                    continue

                # Skip if the track is already in the dataset
                if track_id in ids:
                    continue
                print("Genius API:")
                genius_song = genius.search_song(track_name, track_artist)
                if genius_song:
                    lyrics = genius_song.lyrics
                    add_path = "with_lyrics"
                else:
                    lyrics = ""
                    add_path = "no_lyrics"
                
                song_info = {
                    "available_markets": available_markets,
                    "explicit": explicit,
                    "track_id": track_id,
                    "release_date": release_date,
                    "track_artist": track_artist,
                    "artist_id": artist_id,
                    "track_name": track_name,
                    "album_name": album_name,
                    "album_id": album_id,
                    "duration_ms": duration_ms,
                    "popularity": popularity,
                    "lyrics": lyrics
                }

                with open(f"tracks/{add_path}/{track_id}.json", "w") as f:
                    json.dump(song_info, f)

        except Exception as e:
            print(f"Error processing playlist {playlist}")
            print(e)
            continue
        print("---"*10)

