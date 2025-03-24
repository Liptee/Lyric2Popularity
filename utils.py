import os
import re
from typing import List, Dict
from glob import glob
import json
import pandas as pd


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