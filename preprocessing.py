import json
import re
import os


def process_json_files(folder_path):
    """Обрабатывает все JSON-файлы в указанной папке, очищает текст и выводит результат."""

    for file_name in os.listdir(folder_path):
        if not file_name.endswith(".json"):
            continue  # Пропускаем не JSON-файлы

        file_path = os.path.join(folder_path, file_name)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_content = f.read()  # Читаем файл как строку

            try:
                data = json.loads(raw_content)  # Пробуем распарсить JSON
            except json.JSONDecodeError as e:
                print(f"❌ Ошибка JSON в файле {file_name}: {e}")
                print(
                    f"🔍 Содержимое файла:\n{raw_content[:500]}...\n"
                )  # Выведем первые 500 символов
                data = {}  # Если JSON сломан, создаём пустой словарь

            # Берём текст (если `lyrics` нет, просто пустая строка)
            lyrics = data.get("lyrics", "").strip().lower()

            # Очищаем текст (оставляем только буквы и пробелы)
            clean_lyrics = re.sub(r"[^a-zа-я\s]", "", lyrics)

            print(f"\n--- {file_name} ---\n{clean_lyrics or '⚠️ Нет текста'}")

        except Exception as e:
            print(f"❌ Ошибка с файлом {file_name}: {e}")
