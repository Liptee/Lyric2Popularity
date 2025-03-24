import fasttext
from env import DATA_DIR
import os
from preprocessing import process_json_file


class LanguageIdentification:
    def __init__(self):
        pretrained_lang_model = "lid.176.bin"
        self.model = fasttext.load_model(pretrained_lang_model)

    def predict_lang(self, text):
        predictions = self.model.predict(text, k=5)  # returns top 2 matching languages
        predictions = {
            predictions[0][i].split("__")[-1]: round(predictions[1][i], 4)
            for i in range(5)
        }
        return predictions


if __name__ == "__main__":
    for file in os.listdir(DATA_DIR)[:1000]:
        text = process_json_file(os.path.join(DATA_DIR, "0ma7lbs8BsVIv2kSaqOsDI.json"))
        text = text.encode().decode("unicode_escape")  # ← ВАЖНО
        text = text.replace("\n", " ").strip()
        # predict language
        LANGUAGE = LanguageIdentification()
        predictions = LANGUAGE.predict_lang(text)
        print(file, ":", predictions)
