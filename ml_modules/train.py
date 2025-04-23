from tqdm import tqdm
import torch


def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss = 0.0
    for batch in tqdm(loader, desc="Train"):
        optimizer.zero_grad()
        text = batch["text"].to(device)
        lengths = batch["length"].to(device) if "length" in batch else None
        labels = batch["label"].to(device)
        preds = model(text, lengths) if lengths is not None else model(text)
        loss = criterion(preds, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)


def eval_epoch(model, loader, criterion, device, target_metric):
    model.eval()
    preds, targets, total_loss = [], [], 0.0
    with torch.no_grad():
        for batch in tqdm(loader, desc="Eval"):
            text = batch["text"].to(device)
            lengths = batch["length"].to(device) if "length" in batch else None
            labels = batch["label"].to(device)
            outputs = model(text, lengths) if lengths is not None else model(text)
            total_loss += criterion(outputs, labels).item()
            preds.extend(outputs.cpu().numpy())
            targets.extend(labels.cpu().numpy())
    metric = target_metric(targets, preds, squared=False)
    return total_loss / len(loader), metric