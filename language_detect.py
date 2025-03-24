import fasttext
from env import DATA_DIR, PATH_TO_LANG_MODEL
import os
from preprocessing import process_json_file
from typing import Dict
import json
from tqdm import tqdm
import ftfy


class LanguageIdentification:
    def __init__(self):
        pretrained_lang_model = PATH_TO_LANG_MODEL
        self.model = fasttext.load_model(pretrained_lang_model)

    def predict_lang(self, text):
        predictions = self.model.predict(text, k=3)  # returns top 2 matching languages
        predictions = {
            predictions[0][i].split("__")[-1]: round(predictions[1][i], 4)
            for i in range(len(predictions[0]))
        }
        return predictions
    
def safe_decode(text: str) -> str:
    return ftfy.fix_text(text)

def detect_lang(model: LanguageIdentification, 
                text: str, 
                threshold: float) -> Dict:
    text = text.replace("\n", " ").strip()
    pred = model.predict_lang(text)
    targets = list(pred.keys())
    for lang in targets:
        if pred[lang] < threshold:
            del pred[lang]
    return list(pred.keys())


def make_language_mapping(path_to_dir, path_to_save, threshold):
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
    make_language_mapping(DATA_DIR, "tracks", 0.6)
        

