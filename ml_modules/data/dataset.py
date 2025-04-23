from torch.utils.data import Dataset
from typing import Dict
import numpy as np
import torch

from ml_modules.tokenizers.basic_tokenizer import basic_tokenizer


class LyricsDataset(Dataset):
    def __init__(
        self,
        texts: np.ndarray,
        labels: np.ndarray,
        vocab: Dict[str, int],
        max_len: int,
        unk_token: str,
        pad_token: str
    ):
        self.texts = texts
        self.labels = labels
        self.vocab = vocab
        self.max_len = max_len
        self.unk_token = unk_token
        self.pad_token = pad_token

    def __len__(self) -> int:
        return len(self.texts)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        tokens = basic_tokenizer(self.texts[idx])
        ids = [self.vocab.get(t, self.vocab[self.unk_token]) for t in tokens[: self.max_len]]
        pad_len = self.max_len - len(ids)
        ids += [self.vocab[self.pad_token]] * pad_len
        return {
            "text": torch.tensor(ids, dtype=torch.long),
            "length": torch.tensor(min(len(tokens), self.max_len)),
            "label": torch.tensor(self.labels[idx], dtype=torch.float),
        }