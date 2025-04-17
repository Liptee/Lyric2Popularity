import os
import json
import spacy
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

# === Settings ===
LYRICS_DIR = "tracks/with_lyrics"
MAX_LINES = 20
TOP_N = 10
NUM_FILES = 10

# === Load models ===
def load_models():
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")
    keybert_model = KeyBERT(SentenceTransformer('distilbert-base-nli-mean-tokens', device='cpu'))
    return nlp, keybert_model

# === Helpers ===
def truncate(text, max_lines=MAX_LINES):
    return "\n".join(text.strip().split("\n")[:max_lines])

# === Keyword extraction functions ===
def extract_keywords_tfidf(text, top_n=TOP_N):
    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
        X = vectorizer.fit_transform([text])
        tfidf_scores = X.toarray()[0]
        words = vectorizer.get_feature_names_out()
        word_scores = list(zip(words, tfidf_scores))
        sorted_words = sorted(word_scores, key=lambda x: -x[1])
        return [w for w, _ in sorted_words[:top_n]]
    except:
        return []

def extract_textrank(text, nlp, top_n=TOP_N):
    doc = nlp(text)
    return [phrase.text for phrase in doc._.phrases[:top_n]]

def extract_keybert(text, keybert_model, top_n=TOP_N):
    try:
        keywords = keybert_model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 1),
            stop_words="english",
            top_n=top_n
        )
        return [kw for kw, _ in keywords]
    except Exception as e:
        return [f"⚠️ error: {e}"]

# === Main processing function ===
def process_lyrics(lyrics_dir=LYRICS_DIR, num_files=NUM_FILES, max_lines=MAX_LINES, top_n=TOP_N):
    nlp, keybert_model = load_models()
    files = sorted([f for f in os.listdir(lyrics_dir) if f.endswith(".json")])
    files = files[:num_files]
    
    results = []
    
    for file in tqdm(files, desc="Comparing TF-IDF / TextRank / KeyBERT"):
        track_id = file.replace(".json", "")
        try:
            with open(os.path.join(lyrics_dir, file), "r", encoding="utf-8") as f:
                data = json.load(f)
                lyrics = data.get("lyrics", "")
                if not lyrics.strip():
                    continue
                
                text = truncate(lyrics, max_lines)
                tfidf_tags = extract_keywords_tfidf(text, top_n)
                textrank_tags = extract_textrank(text, nlp, top_n)
                keybert_tags = extract_keybert(text, keybert_model, top_n)
                
                result = {
                    "track_id": track_id,
                    "lyrics_snippet": text,
                    "tfidf_tags": tfidf_tags,
                    "textrank_tags": textrank_tags,
                    "keybert_tags": keybert_tags
                }
                results.append(result)
                
                # Вывод для отображения прогресса
                print(f"\n🎵 {track_id}")
                print(f"TF-IDF → {tfidf_tags}")
                print(f"TextRank → {textrank_tags}")
                print(f"KeyBERT → {keybert_tags}")
                
        except Exception as e:
            print(f"⚠️ Error in file {file}: {e}")
    
    return results

# Функция для запуска из командной строки
def main():
    process_lyrics()

if __name__ == "__main__":
    main()