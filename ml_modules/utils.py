import torch
import shutil

from env import CHECKPOINT_DIR


def save_checkpoint(state: dict, is_best: bool, filename: str):
    """Save model checkpoint and copy best to 'best_checkpoint.pth'."""
    filepath = CHECKPOINT_DIR / filename
    torch.save(state, filepath)
    if is_best:
        shutil.copyfile(filepath, CHECKPOINT_DIR / "best_checkpoint.pth")