import fasttext
from env import PATH_TO_LANG_MODEL
import ftfy
from typing import Dict


class LanguageIdentification:
    def __init__(self):
        pretrained_lang_model = PATH_TO_LANG_MODEL
        self.model = fasttext.load_model(pretrained_lang_model)

    def predict_lang(self, text):
        predictions = self.model.predict(text, k=3)  # returns top k matching languages
        predictions = {
            predictions[0][i].split("__")[-1]: round(predictions[1][i], 4)
            for i in range(len(predictions[0]))
        }
        return predictions
    

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


def safe_decode(text: str) -> str:
    """
    Cause we have texts on many languages, we need to decode them to utf-8
    This function is used to decode the text to utf-8 correctly
    """
    return ftfy.fix_text(text)