import fasttext
from env import DATA_DIR
import os
from preprocessing import process_json_file

class LanguageIdentification:
    def __init__(self):
        pretrained_lang_model = "language_models/lid.176.bin"
        self.model = fasttext.load_model(pretrained_lang_model)

    def predict_lang(self, text):
        predictions = self.model.predict(text, k=5) # returns top 2 matching languages
        predictions = {predictions[0][i].split("__")[-1]: round(predictions[1][i], 4) for i in range(5)}
        return predictions

if __name__ == '__main__':
    for file in os.listdir(DATA_DIR):
        text = process_json_file(os.path.join(DATA_DIR, file))

        # remove \n
        text = text.replace("\n", "")
        # predict language
        LANGUAGE = LanguageIdentification()
        predictions = LANGUAGE.predict_lang(text)
        print(predictions)

