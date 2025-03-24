import json
import re


# TODO: process parts of lyrics
# TODO: process stop words


def process_json_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "lyrics" in data:
            return processing_lyrics(data["lyrics"])
        return ""
    except Exception as e:
        print(f"Read error – {file_path}: {e}")
        return


def processing_lyrics(text: str) -> str:
    # text = text.strip().lower()
    # text = delete_parts_of_lyrics(text)
    # text = re.sub(r"[^a-zа-я\s]", "", text)
    return text



