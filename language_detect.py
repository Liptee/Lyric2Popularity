import fasttext

class LanguageIdentification:

    def __init__(self):
        pretrained_lang_model = "language_models/lid.176.bin"
        self.model = fasttext.load_model(pretrained_lang_model)

    def predict_lang(self, text):
        predictions = self.model.predict(text, k=5) # returns top 2 matching languages
        predictions = {predictions[0][i].split("__")[-1]: round(predictions[1][i], 4) for i in range(5)}
        return predictions

if __name__ == '__main__':
    LANGUAGE = LanguageIdentification()
    lang = LANGUAGE.predict_lang("Привет, как дела?")
    print(lang)