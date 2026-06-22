"""
Etapa 2 — CNN Encoder/Decoder para ETH-80.
Encoder: ResNet18 pretrained -> 64-dim latent vector.
Decoder: ConvTranspose -> 128x128x3.
Loss: MSE reconstrucción + CrossEntropy clasificación.
"""
import json
import sys
import os
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data" / "eth80"
MODELS_DIR = ROOT / "models"
MODELS_DIR.mkdir(exist_ok=True)

CLASSES = ["apple", "horse", "car"]
CLASS_TO_IDX = {c: i for i, c in enumerate(CLASSES)}
LATENT_DIM = 64
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 50
LR = 1e-3
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class ETH80Dataset(Dataset):
    def __init__(self, image_paths, transform=None):
        self.paths = image_paths
        self.transform = transform

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        path = self.paths[idx]
        img = Image.open(path).convert("RGB").resize((IMG_SIZE, IMG_SIZE))
        # extract class from path
        cls = Path(path).parent.name
        label = CLASS_TO_IDX[cls]
        if self.transform:
            img = self.transform(img)
        return img, label


class Encoder(nn.Module):
    def __init__(self, latent_dim=LATENT_DIM):
        super().__init__()
        backbone = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        # Remove final FC, keep up to avgpool -> 512-dim
        self.features = nn.Sequential(*list(backbone.children())[:-1])
        self.fc = nn.Linear(512, latent_dim)

    def forward(self, x):
        f = self.features(x)         # (B, 512, 1, 1)
        f = f.view(f.size(0), -1)    # (B, 512)
        z = self.fc(f)               # (B, latent_dim)
        return z


class Decoder(nn.Module):
    """ConvTranspose2d decoder: 64-dim -> 128x128x3."""
    def __init__(self, latent_dim=LATENT_DIM):
        super().__init__()
        self.fc = nn.Linear(latent_dim, 512 * 4 * 4)
        self.deconv = nn.Sequential(
            # 4x4 -> 8x8
            nn.ConvTranspose2d(512, 256, 4, stride=2, padding=1),
            nn.BatchNorm2d(256), nn.ReLU(),
            # 8x8 -> 16x16
            nn.ConvTranspose2d(256, 128, 4, stride=2, padding=1),
            nn.BatchNorm2d(128), nn.ReLU(),
            # 16x16 -> 32x32
            nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1),
            nn.BatchNorm2d(64), nn.ReLU(),
            # 32x32 -> 64x64
            nn.ConvTranspose2d(64, 32, 4, stride=2, padding=1),
            nn.BatchNorm2d(32), nn.ReLU(),
            # 64x64 -> 128x128
            nn.ConvTranspose2d(32, 3, 4, stride=2, padding=1),
            nn.Sigmoid(),
        )

    def forward(self, z):
        x = self.fc(z)
        x = x.view(-1, 512, 4, 4)
        return self.deconv(x)


class Classifier(nn.Module):
    def __init__(self, latent_dim=LATENT_DIM, n_classes=len(CLASSES)):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(latent_dim, 64),
            nn.ReLU(),
            nn.Linear(64, n_classes),
        )

    def forward(self, z):
        return self.fc(z)


def get_loaders():
    splits_path = DATA_DIR / "splits.json"
    splits = json.loads(splits_path.read_text())

    transform_train = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(0.2, 0.2, 0.2),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    train_paths = []
    test_paths = []
    for cls in CLASSES:
        train_paths += splits[cls]["train"]
        test_paths += splits[cls]["test"]

    train_ds = ETH80Dataset(train_paths, transform_train)
    test_ds = ETH80Dataset(test_paths, transform_test)
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)
    return train_loader, test_loader


def train():
    print(f"Training on {DEVICE}")
    train_loader, test_loader = get_loaders()

    encoder = Encoder().to(DEVICE)
    decoder = Decoder().to(DEVICE)
    classifier = Classifier().to(DEVICE)

    params = list(encoder.parameters()) + list(decoder.parameters()) + list(classifier.parameters())
    optimizer = optim.Adam(params, lr=LR)
    mse_loss = nn.MSELoss()
    ce_loss = nn.CrossEntropyLoss()

    # Inverse normalize for reconstruction comparison
    inv_norm = transforms.Normalize(
        mean=[-0.485/0.229, -0.456/0.224, -0.406/0.225],
        std=[1/0.229, 1/0.224, 1/0.225])

    best_rmse = float("inf")
    for epoch in range(1, EPOCHS + 1):
        encoder.train(); decoder.train(); classifier.train()
        total_loss = 0.0
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
            # denormalize for MSE target
            imgs_orig = torch.stack([inv_norm(img) for img in imgs]).clamp(0, 1)

            optimizer.zero_grad()
            z = encoder(imgs)
            recon = decoder(z)
            logits = classifier(z)

            loss_recon = mse_loss(recon, imgs_orig)
            loss_cls = ce_loss(logits, labels)
            loss = loss_recon + 0.1 * loss_cls
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * len(imgs)

        avg_loss = total_loss / len(train_loader.dataset)
        if epoch % 10 == 0:
            rmse, acc = evaluate(encoder, decoder, classifier, test_loader, inv_norm)
            print(f"Epoch {epoch:3d}/{EPOCHS}  loss={avg_loss:.4f}  "
                  f"RMSE={rmse:.4f}  acc={acc:.1f}%")
            if rmse < best_rmse:
                best_rmse = rmse
                save_models(encoder, decoder, classifier)

    # Final evaluation
    rmse, acc = evaluate(encoder, decoder, classifier, test_loader, inv_norm)
    print(f"\nFinal  RMSE={rmse:.4f}  acc={acc:.1f}%")
    return rmse, acc, encoder, decoder, classifier


def evaluate(encoder, decoder, classifier, loader, inv_norm):
    encoder.eval(); decoder.eval(); classifier.eval()
    mse_total = 0.0
    correct = 0
    n = 0
    with torch.no_grad():
        for imgs, labels in loader:
            imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
            imgs_orig = torch.stack([inv_norm(img) for img in imgs]).clamp(0, 1)
            z = encoder(imgs)
            recon = decoder(z)
            logits = classifier(z)
            # per-pixel MSE: sum over all pixels, divide by n*H*W*C later
            mse_total += nn.MSELoss(reduction="mean")(recon, imgs_orig).item() * len(imgs)
            correct += (logits.argmax(1) == labels).sum().item()
            n += len(imgs)
    rmse = (mse_total / n) ** 0.5   # per-pixel RMSE in [0,1] range
    acc = 100.0 * correct / n
    return rmse, acc


def save_models(encoder, decoder, classifier):
    torch.save(encoder.state_dict(), MODELS_DIR / "encoder.pt")
    torch.save(decoder.state_dict(), MODELS_DIR / "decoder.pt")
    torch.save(classifier.state_dict(), MODELS_DIR / "classifier.pt")
    print("  Models saved.")


def load_models():
    encoder = Encoder().to(DEVICE)
    decoder = Decoder().to(DEVICE)
    classifier = Classifier().to(DEVICE)
    encoder.load_state_dict(torch.load(MODELS_DIR / "encoder.pt", map_location=DEVICE))
    decoder.load_state_dict(torch.load(MODELS_DIR / "decoder.pt", map_location=DEVICE))
    classifier.load_state_dict(torch.load(MODELS_DIR / "classifier.pt", map_location=DEVICE))
    encoder.eval(); decoder.eval(); classifier.eval()
    return encoder, decoder, classifier


def visualize_reconstructions(encoder, decoder, test_loader, n=5):
    """Save a grid of original vs reconstructed images."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    inv_norm = transforms.Normalize(
        mean=[-0.485/0.229, -0.456/0.224, -0.406/0.225],
        std=[1/0.229, 1/0.224, 1/0.225])

    encoder.eval(); decoder.eval()
    imgs, labels = next(iter(test_loader))
    imgs = imgs[:n].to(DEVICE)
    with torch.no_grad():
        z = encoder(imgs)
        recon = decoder(z)

    fig, axes = plt.subplots(2, n, figsize=(3*n, 6))
    for i in range(n):
        orig = inv_norm(imgs[i].cpu()).clamp(0, 1).permute(1, 2, 0).numpy()
        rec = recon[i].cpu().permute(1, 2, 0).numpy()
        axes[0, i].imshow(orig); axes[0, i].set_title(f"orig {CLASSES[labels[i]]}")
        axes[1, i].imshow(rec); axes[1, i].set_title("recon")
        for ax in [axes[0, i], axes[1, i]]:
            ax.axis("off")
    plt.tight_layout()
    out = ROOT / "stage2_reconstructions.png"
    plt.savefig(out, dpi=80)
    print(f"Reconstructions saved to {out}")


def get_prototype_latent(encoder, cls: str) -> np.ndarray:
    """Return mean latent vector for all training images of a class."""
    splits_path = DATA_DIR / "splits.json"
    splits = json.loads(splits_path.read_text())
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    paths = splits[cls]["train"]
    zs = []
    encoder.eval()
    with torch.no_grad():
        for p in paths:
            img = Image.open(p).convert("RGB").resize((IMG_SIZE, IMG_SIZE))
            img = transform(img).unsqueeze(0).to(DEVICE)
            z = encoder(img).cpu().numpy()[0]
            zs.append(z)
    return np.mean(zs, axis=0)


if __name__ == "__main__":
    if (MODELS_DIR / "encoder.pt").exists():
        print("Models already trained. Loading for evaluation...")
        encoder, decoder, classifier = load_models()
        _, test_loader = get_loaders()
        inv_norm = transforms.Normalize(
            mean=[-0.485/0.229, -0.456/0.224, -0.406/0.225],
            std=[1/0.229, 1/0.224, 1/0.225])
        rmse, acc = evaluate(encoder, decoder, classifier, test_loader, inv_norm)
        print(f"RMSE={rmse:.4f}  acc={acc:.1f}%")
    else:
        rmse, acc, encoder, decoder, classifier = train()

    _, test_loader = get_loaders()
    visualize_reconstructions(encoder, decoder, test_loader)

    if rmse >= 0.3:
        print(f"WARNING: RMSE={rmse:.4f} >= 0.3 — consider more training epochs.")
    if acc < 85.0:
        print(f"WARNING: accuracy={acc:.1f}% < 85% — consider more training epochs.")

    if rmse < 0.3 and acc >= 85.0:
        print("\nEtapa 2 COMPLETADA.")
    else:
        print("\nEtapa 2 no cumple criterios — ajustar hiperparámetros.")
