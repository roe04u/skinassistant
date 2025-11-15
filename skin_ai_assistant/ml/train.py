import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from pathlib import Path
import mlflow
import mlflow.pytorch
import json

from backend.config import BASE_DIR, MODELS_DIR, BEST_MODEL

DATA = BASE_DIR / "dataset"

def load_data():
    transform_train = transforms.Compose([
        transforms.Resize((256,256)),
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])

    transform_val = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])

    train_ds = datasets.ImageFolder(DATA/'train', transform_train)
    val_ds = datasets.ImageFolder(DATA/'val', transform_val)

    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=32, shuffle=False)

    return train_loader, val_loader, train_ds.classes

def train():
    train_loader, val_loader, classes = load_data()

    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
    model.fc = nn.Linear(model.fc.in_features, len(classes))

    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=1e-4)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    best_acc = 0
    EPOCHS = 8

    for epoch in range(EPOCHS):
        model.train()
        total, correct = 0, 0

        for x,y in train_loader:
            x,y = x.to(device), y.to(device)
            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out,y)
            loss.backward()
            optimizer.step()

        # Eval
        model.eval()
        val_correct, val_total = 0, 0
        with torch.no_grad():
            for x,y in val_loader:
                x,y = x.to(device), y.to(device)
                out = model(x)
                pred = out.argmax(1)
                val_correct += (pred==y).sum().item()
                val_total += len(y)

        acc = val_correct/val_total
        print("Epoch", epoch, "Acc", acc)

        if acc > best_acc:
            best_acc = acc
            torch.save({
                "model": model.state_dict(),
                "classes": classes
            }, MODELS_DIR/"best_model.pt")

    # Export ONNX
    dummy = torch.randn(1,3,224,224).to(device)
    model.eval()
    torch.onnx.export(
        model,
        dummy,
        BEST_MODEL,
        input_names=["input"],
        output_names=["logits"],
        dynamic_axes={"input":{0:"batch"}, "logits":{0:"batch"}},
        opset_version=17
    )

    # Save labels
    (MODELS_DIR/"best"/"class_names.txt").write_text("\n".join(classes))

if __name__ == "__main__":
    train()