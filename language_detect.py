import fasttext

class LanguageIdentification:

    def __init__(self):
        pretrained_lang_model = "language_models/lid.176.bin"
        self.model = fasttext.load_model(pretrained_lang_model)

    def predict_lang(self, text):
        predictions = self.model.predict(text, k=2) # returns top 2 matching languages
        return predictions

if __name__ == '__main__':
    LANGUAGE = LanguageIdentification()
    lang = LANGUAGE.predict_lang("Hej")
    print(lang)