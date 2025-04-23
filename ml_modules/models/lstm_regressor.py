import torch
import torch.nn as nn


class LSTMRegressor(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        embed_dim: int,
        hidden_dim: int,
        num_layers: int,
        dropout: float,
        pad_idx: int
    ):
        super().__init__()

        self.embedding = nn.Embedding(
            vocab_size, 
            embed_dim, 
            padding_idx=pad_idx)
        
        self.lstm = nn.LSTM(
            embed_dim, hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0.0
        )

        self.fc = nn.Linear(hidden_dim * 2, 1)
        self.dropout = nn.Dropout(dropout)

    def forward(
            self, 
            text: torch.Tensor, 
            lengths: torch.Tensor) -> torch.Tensor:
        emb = self.embedding(text)
        packed = nn.utils.rnn.pack_padded_sequence(
            emb, 
            lengths.cpu(), 
            batch_first=True, 
            enforce_sorted=False
        )
        _, (h, _) = self.lstm(packed)
        h = torch.cat((h[-2], h[-1]), dim=1)
        return self.fc(self.dropout(h)).squeeze()