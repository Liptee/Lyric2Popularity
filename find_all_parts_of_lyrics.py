import json
import re
import os
from tqdm import tqdm


parts_of_lyrics = set()

dir_path = "/Users/mac/Desktop/Recommended System/tracks/with_lyrics"

for file_name in tqdm(os.listdir(dir_path)):
    if not file_name.endswith(".json"):
        continue

    file_path = os.path.join(dir_path, file_name)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "lyrics" in data:
        lyrics = data["lyrics"]
        # find in lyrics part with [<PART_OF_LYRICS>] pattern
        song_parts_of_lyrics = re.findall(r'\[(.*?)\]', lyrics)
        parts_of_lyrics.update(song_parts_of_lyrics)

print(parts_of_lyrics)
