import json
import re
import os

folder_path = "/Users/royalskifm/Downloads/Spotify"

for file_name in os.listdir(folder_path):
    if not file_name.endswith(".json"):
        continue  # Пропускаем не JSON-файлы

    file_path = os.path.join(folder_path, file_name)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        lyrics = data.get("lyrics", "").strip().lower()  # Приводим к нижнему регистру
        if not lyrics:
            continue  # Пропускаем файлы без текста

        # Очищаем текст (оставляем только буквы и пробелы)
        clean_lyrics = re.sub(r"[^a-zа-я\s]", "", lyrics)

        print(f"\n--- {file_name} ---\n{clean_lyrics}")

    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"❌ Ошибка в файле {file_name}: {e}")
