import os
import re
from typing import List, Dict
from glob import glob
import json
import pandas as pd

all_fields = [
    "available_markets",
    "explicit",
    "track_id",
    "release_date",
    "track_artist",
    "artist_id",
    "track_name",
    "album_name",
    "album_id",
    "duration_ms",
    "popularity",
    "lyrics"
]


def load_json_data(file_path: str, columns: List) -> Dict:
    with open(file_path, "r") as f:
        data = json.load(f)
        dict_data = {}
        for column in columns:
            dict_data[column] = data[column]
        return dict_data


def load_jsons_data(data_dir: str, columns: List) -> pd.DataFrame:
    data_list = []
    for file_path in glob(os.path.join(data_dir, "*.json")):
        data_list.append(load_json_data(
            file_path=file_path,
            columns=columns
        ))
    return pd.DataFrame(data_list)


def delete_parts_of_lyrics(text: str) -> str:
    parts_of_lyrics = re.findall(r'\[(.*?)\]', text)
    for part in parts_of_lyrics:
        text = text.replace(f"[{part}]", "")
    return text


def convert_jsons_to_csv(data_dir: str, columns: List) -> pd.DataFrame:
    data = []
    for file in glob(os.path.join(data_dir, "*.json")):
        json_data = load_json_data(
            file_path=file,
            columns=columns)
        data.append(json_data)
    
    # data_to_csv
    df = pd.DataFrame(data)
    df.to_csv("tracks_data.csv", index=False)
    return df