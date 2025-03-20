import json
import re
import os


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
    text = text.strip().lower()
    # text = re.sub(r"[^a-zа-я\s]", "", text)
    return text


if __name__ == "__main__":
    a = process_json_file("/Users/mac/Desktop/Recommended System/tracks/with_lyrics/0A189BUGs0WHvEA09bWdA6.json")
    print(a)


