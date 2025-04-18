import spacy
import pytextrank
from keybert import KeyBERT
from typing import List, Dict
from rake_nltk import Rake
from yake import KeywordExtractor
from collections import Counter
from string import punctuation


rake = Rake()
yake = KeywordExtractor()
pure_spacy = spacy.load("en_core_web_sm")
keybert_nlp = KeyBERT("distilbert-base-nli-mean-tokens")
textrank_nlp = spacy.load("en_core_web_sm")
textrank_nlp.add_pipe("textrank")


def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
    doc = pure_spacy(text.lower()) 
    for token in doc:
        if(token.text in pure_spacy.Defaults.stop_words or token.text in punctuation): continue
        if(token.pos_ in pos_tag): result.append(token.text)
    return result

def keybert_keywords(text: str, threshold: float = 0.1) -> Dict[str, float]:
    keywords = keybert_nlp.extract_keywords(text)
    return {keyword: score for keyword, score in keywords if score >= threshold}

def textrank_keywords(text: str, threshold: float = 0.1) -> Dict[str, float]:
    doc = textrank_nlp(text)
    keywords = {}
    for phrase in doc._.phrases:
        if phrase.rank >= threshold:
            keywords[phrase.text] = phrase.rank
    return keywords

def rake_keywords(text: str, threshold: float = 1.0) -> Dict[str, float]:
    rake.extract_keywords_from_text(text)
    keywords = rake.get_ranked_phrases_with_scores()
    res = {}
    for score, kw in keywords:
        if float(score) >= threshold:
            res[kw] = float(score)
    return res

def yake_keywords(text: str, threshold: float = 0.1) -> Dict[str, float]:
    keywords = yake.extract_keywords(text)
    res = {}
    for kw, score in keywords:
        if score >= threshold:
            res[kw] = score
    return res

def spacy_keywords(text: str, limit: int = 10) -> Dict[str, float]:
    output = set(get_hotwords(text))
    most_common = Counter(output).most_common(limit)
    return dict(most_common)