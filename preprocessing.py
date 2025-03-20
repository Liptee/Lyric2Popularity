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

def delete_parts_of_lyrics(text: str) -> str:
    parts_of_lyrics = re.findall(r'\[(.*?)\]', text)
    for part in parts_of_lyrics:
        text = text.replace(f"[{part}]", "")
    return text

def processing_lyrics(text: str) -> str:
    text = text.strip().lower()
    text = delete_parts_of_lyrics(text)
    text = re.sub(r"[^a-zа-я\s]", "", text)
    return text


if __name__ == "__main__":
    text = "1234567890"
    print(replace_numeric_to_text(text))

