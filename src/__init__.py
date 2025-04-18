from src.keyword_modules import *

class KeywordExtractor():
    def __init__(self):
        self.rake = rake_keywords
        self.yake = yake_keywords
        self.keybert = keybert_keywords
        self.textrank = textrank_keywords
        self.spacy = spacy_keywords