from env import DATA_DIR
import os
from preprocessing import process_json_file
import json
from tqdm import tqdm
from src.lang_identification import LanguageIdentification, detect_lang, safe_decode


def make_language_mapping(path_to_dir, 
                          path_to_save, 
                          threshold):
    language_model = LanguageIdentification()
    lang_to_files = {}
    for file in tqdm(os.listdir(path_to_dir)):
        text = process_json_file(os.path.join(path_to_dir, file))
        text = safe_decode(text)
        langs = detect_lang(language_model,
                            text,
                            threshold)
        
        if len(langs) == 0:
            langs.append("None")
        for lang in langs:
            if lang not in lang_to_files:
                lang_to_files[lang] = []
            lang_to_files[lang].append(file)
    
    with open(f'{path_to_save}/language_mapping_trh-{threshold}.json', 'w', encoding='utf-8') as f:
        json.dump(lang_to_files, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    make_language_mapping(DATA_DIR, "tracks", 0.8)

