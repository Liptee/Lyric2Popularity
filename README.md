# Predicting Song Popularity Based on Lyrics

## Overview
This project aims to build a machine learning model that predicts a song's popularity based on its lyrics. The project leverages data from Spotify and Genius to collect track information and lyrics.

## Goals
- **Model Development**: Build an algorithm capable of predicting song popularity using its lyrics.
- **Data Collection**: Automatically collect song metadata and lyrics using the Spotify and Genius APIs.
- **Data Preprocessing**: Develop scripts to clean and preprocess the textual data.
- **Analysis & Experiments**: Conduct experiments to identify the most significant features and optimize the model.

## Current Tools and Modules
1. **env.py**: if you want to collecte your own data, you need the API client on **Spotify** and **GeniusLyrics**. Enviroment variables includes:
- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`
- `SPOTIPY_REDIRECT_URI`
- `SPOTIPY_ACCES_TOKEN`
- `GENIUS_CLIENT_ID`
- `GENIUS_CLIENT_SECRET`
- `GENIUS_ACCESS_TOKEN`
2. **check_current_song.py**: Retrieves the currently playing track on Spotify along with its lyrics from Genius.
3. **preprocessing.py**: Contains functions for cleaning song lyrics by removing labels and unwanted characters.
4. **create_dataset_lyrics_popularity.py**: Creates a dataset containing track metadata and lyrics, saving files into `tracks/with_lyrics` and `tracks/no_lyrics` folders. Next, the data collection method will be described. 

The collection tactic is to specify a query to search for user's playlists on Spotify. In `queries` you can specify a list of queries and the first `N` query results will be parsed and tracks will be extracted from them. After extracting the artist and song title, an API request will be sent to **Genius** to find the lyrics. If successful, all track information will be stored in the `with_lyrics` directory, if unsuccessful in the `no_lyrics` directory.

5. **language_detect.py**: Since both **Genius** and **Spotify** not provide infromation about song language we can use a FastText model to identify the language of the given text. It's may be a valuable information for next stage of research.

6. **find_all_parts_of_lyrics.py**: Extracts structural parts of the lyrics (e.g., `[Verse]` – *(Куплет)*, `[Chorus]` – *(Припев)*) for further analysis.

## Future steps
- get minimum error on baseline method (TF-IDF + XGBoost)
- create script for splitting songs by languages
- add model to tag each song (it may be useful for semantic alanlyse and further storage data in Neo4J)
- migrate all data on Neo4J cluster