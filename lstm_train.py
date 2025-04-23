
from datetime import datetime
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from env import DATA_DIR
from src.utils import load_jsons_data
from src.lang_identification import safe_decode
from src.df_filters import DFFilters

from ml_modules.models.lstm_regressor import LSTMRegressor
from ml_modules.data.dataset import LyricsDataset
from ml_modules.tokenizers.basic_tokenizer import build_vocab
from ml_modules.train import train_epoch, eval_epoch
from ml_modules.utils import save_checkpoint

CONFIG = {
    "test_size": 0.2,
    "random_state": 42,
    "min_freq": 2,
    "max_vocab": 20000,
    "max_len": 256,
    "batch_size": 32,
    "lr": 1e-3,
    "epochs": 5,
    "embed_dim": 300,
    "hidden_dim": 256,
    "num_layers": 2,
    "dropout": 0.5,
}

PAD_TOKEN = "<pad>"
UNK_TOKEN = "<unk>"

def preprocess_df():
    df = load_jsons_data(
        data_dir=DATA_DIR,
        columns=["lyrics", "popularity", "track_id"]
    )
    df = DFFilters.popularity(df, 2)
    df = DFFilters.language(
        df,
        mapping_file="tracks/language_mapping_trh-0.6.json",
        white_list=["en"]
    )
    df["lyrics"] = (
        df["lyrics"]
        .apply(safe_decode)
        .str.lower()
        .str.replace(r"[^\w\s]", "", regex=True)
        .str.replace(r"\d+", "", regex=True)
        .str.strip()
    )
    return df[df["lyrics"].astype(bool)]

def main():
    df = preprocess_df()
    X, y = df["lyrics"].values, df["popularity"].values

    X_tr, X_val, y_tr, y_val = train_test_split(
        X, y,
        test_size=CONFIG["test_size"],
        random_state=CONFIG["random_state"]
    )

    vocab = build_vocab(
        X_tr,
        min_freq=CONFIG["min_freq"],
        max_vocab=CONFIG["max_vocab"],
        pad_token=PAD_TOKEN,
        unk_token=UNK_TOKEN
    )
    pad_idx = vocab[PAD_TOKEN]

    train_ds = LyricsDataset(X_tr, y_tr, vocab, CONFIG["max_len"], UNK_TOKEN, PAD_TOKEN)
    val_ds = LyricsDataset(X_val, y_val, vocab, CONFIG["max_len"], UNK_TOKEN, PAD_TOKEN)

    train_loader = DataLoader(train_ds, batch_size=CONFIG["batch_size"], shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=CONFIG["batch_size"])

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = LSTMRegressor(
        vocab_size=len(vocab),
        embed_dim=CONFIG["embed_dim"],
        hidden_dim=CONFIG["hidden_dim"],
        num_layers=CONFIG["num_layers"],
        dropout=CONFIG["dropout"],
        pad_idx=pad_idx
    ).to(device)

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=CONFIG["lr"])

    best_rmse = float("inf")
    for epoch in range(1, CONFIG["epochs"] + 1):
        tr_loss = train_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_rmse = eval_epoch(model, val_loader, criterion, device, mean_squared_error)
        print(f"Epoch {epoch}: train_loss={tr_loss:.4f} val_loss={val_loss:.4f} rmse={val_rmse:.4f}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ckpt_name = f"ckpt_epoch{epoch}_{timestamp}.pth"
        is_best = val_rmse < best_rmse
        save_checkpoint({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'val_rmse': val_rmse,
        }, is_best, ckpt_name)

        if is_best:
            best_rmse = val_rmse

    print(f"Training finished. Best RMSE: {best_rmse:.4f}")


if __name__ == "__main__":
    main()
