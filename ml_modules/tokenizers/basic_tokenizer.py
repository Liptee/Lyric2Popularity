from typing import List, Dict
import re
from collections import Counter


def basic_tokenizer(text: str) -> List[str]:
    return re.findall(r"\b\w+\b", text.lower())


def build_vocab(
        texts: List[str], 
        min_freq: int, 
        max_vocab: int,
        pad_token: str,
        unk_token: str) -> Dict[str, int]:
    cnt = Counter()
    for txt in texts:
        cnt.update(basic_tokenizer(txt))
    vocab = {pad_token: 0, unk_token: 1}
    for word, freq in cnt.most_common():
        if freq < min_freq or len(vocab) >= max_vocab:
            break
        vocab[word] = len(vocab)
    return vocab