"""
single_file_quicktest.py
========================
Self-contained single-file version of the Image Classification project.
Runs all three models (Basic CNN, Improved CNN, Transfer Learning)
on Fashion-MNIST with reduced epochs so you can verify everything works
quickly on any laptop.

Run with:
    python single_file_quicktest.py
"""

import os, warnings, random, time
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
warnings.filterwarnings("ignore")

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, datasets
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.metrics import confusion_matrix, classification_report

# ─────────────────────────────────────────────
# CONFIG (edit here)
# ─────────────────────────────────────────────
DATASET          = "fashion_mnist"   # or "cifar10"
BATCH_SIZE       = 64
EPOCHS           = 8                 # keep low for quick test; increase for full training
LEARNING_RATE    = 1e-3
VALIDATION_SPLIT = 0.1
RANDOM_SEED      = 42
TRANSFER_SIZE    = (96, 96)          # spatial dims for MobileNetV2
NUM_SAMPLES      = 16               # sample predictions grid

OUTPUT_DIR       = "quick_outputs"
os.makedirs(f"{OUTPUT_DIR}/plots",   exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/models",  exist_ok=True)

FASHION_CLASSES  = ["T-shirt","Trouser","Pullover","Dress","Coat",
                    "Sandal","Shirt","Sneaker","Bag","Ankle boot"]
CIFAR10_CLASSES  = ["Airplane","Auto","Bird","Cat","Deer",
                    "Dog","Frog","Horse","Ship","Truck"]

# ─────────────────────────────────────────────
# Reproducibility
# ─────────────────────────────────────────────
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
def load_data(for_transfer=False):
    if DATASET == "fashion_mnist":
        (xtr, ytr), (xte, yte) = datasets.fashion_mnist.load_data()
        class_names = FASHION_CLASSES
    else:
        (xtr, ytr), (xte, yte) = datasets.cifar10.load_data()
        ytr, yte = ytr.flatten(), yte.flatten()
        class_names = CIFAR10_CLASSES

    # Add channel + normalise
    if xtr.ndim == 3:
        xtr = xtr[..., np.newaxis]
        xte = xte[..., np.newaxis]
    xtr = xtr.astype("float32") / 255.0
    xte = xte.astype("float32") / 255.0

    # Validation split
    np.random.seed(RANDOM_SEED)
    idx  = np.random.permutation(len(xtr))
    n_val = int(len(xtr) * VALIDATION_SPLIT)
    xval, yval = xtr[idx[:n_val]], ytr[idx[:n_val]]
    xtr,  ytr  = xtr[idx[n_val:]], ytr[idx[n_val:]]

    if for_transfer:
        h, w = TRANSFER_SIZE
        def resize(x):
            x = tf.image.resize(tf.constant(x, tf.float32), [h, w]).numpy()
            if x.shape[-1] == 1:
                x = np.concatenate([x]*3, axis=-1)
            return x
        print("  Resizing for transfer learning …")
        xtr, xval, xte = resize(xtr), resize(xval), resize(xte)
        shape = (h, w, 3)
    else:
        shape = xtr.shape[1:]

    print(f"  Train {xtr.shape} | Val {xval.shape} | Test {xte.shape}")
    return xtr, ytr, xval, yval, xte, yte, class_names, shape

# ─────────────────────────────────────────────
# MODELS
# ─────────────────────────────────────────────
def basic_cnn(input_shape, num_classes):
    m = models.Sequential([
        layers.Conv2D(32, 3, activation="relu", padding="same", input_shape=input_shape),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation="relu", padding="same"),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dense(num_classes, activation="softmax"),
    ], name="Basic_CNN")
    return m

def improved_cnn(input_shape, num_classes):
    inp = layers.Input(shape=input_shape)
    x = layers.RandomFlip("horizontal")(inp)
    x = layers.RandomRotation(0.1)(x)
    for filters in [32, 64, 128]:
        x = layers.Conv2D(filters, 3, padding="same", use_bias=False)(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation("relu")(x)
        x = layers.Conv2D(filters, 3, padding="same", use_bias=False)(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation("relu")(x)
        if filters < 128:
            x = layers.MaxPooling2D()(x)
        x = layers.Dropout(0.25)(x)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, use_bias=False)(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.Dropout(0.5)(x)
    out = layers.Dense(num_classes, activation="softmax")(x)
    return models.Model(inp, out, name="Improved_CNN")

def transfer_model(input_shape, num_classes):
    base = MobileNetV2(input_shape=input_shape, include_top=False, weights="imagenet")
    base.trainable = False
    inp = layers.Input(shape=input_shape)
    x   = layers.Rescaling(2.0, -1.0)(inp)
    x   = base(x, training=False)
    x   = layers.GlobalAveragePooling2D()(x)
    x   = layers.Dense(256, activation="relu")(x)
    x   = layers.Dropout(0.4)(x)
    out = layers.Dense(num_classes, activation="softmax")(x)
    return models.Model(inp, out, name="Transfer_MobileNetV2")

# ─────────────────────────────────────────────
# TRAINING
# ─────────────────────────────────────────────
def train(model, xtr, ytr, xval, yval, save_path):
    model.compile(optimizer=optimizers.Adam(LEARNING_RATE),
                  loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    model.summary(line_length=70)
    cbs = [
        EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True, verbose=1),
        ModelCheckpoint(save_path, monitor="val_accuracy", save_best_only=True, verbose=0),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, min_lr=1e-7, verbose=1),
    ]
    t0 = time.time()
    h  = model.fit(xtr, ytr, validation_data=(xval, yval),
                   epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=cbs, verbose=1)
    return h, time.time() - t0

# ─────────────────────────────────────────────
# VISUALISATION
# ─────────────────────────────────────────────
def plot_history(h, name):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle(f"Training History – {name}", fontweight="bold")
    axes[0].plot(h.history["accuracy"],     label="Train")
    axes[0].plot(h.history["val_accuracy"], label="Val", linestyle="--")
    axes[0].set_title("Accuracy"); axes[0].legend(); axes[0].grid(True, alpha=.3)
    axes[1].plot(h.history["loss"],     label="Train")
    axes[1].plot(h.history["val_loss"], label="Val", linestyle="--")
    axes[1].set_title("Loss"); axes[1].legend(); axes[1].grid(True, alpha=.3)
    plt.tight_layout()
    path = f"{OUTPUT_DIR}/plots/{name.replace(' ','_')}_history.png"
    fig.savefig(path, dpi=120); plt.close(fig)
    print(f"  History plot → {path}")

def plot_cm(yt, yp, class_names, name):
    cm = confusion_matrix(yt, yp).astype(float)
    cm = cm / cm.sum(axis=1, keepdims=True)
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(cm, annot=True, fmt=".2f", cmap="Blues",
                xticklabels=class_names, yticklabels=class_names, ax=ax)
    ax.set_title(f"Confusion Matrix – {name}", fontweight="bold")
    ax.set_xlabel("Predicted"); ax.set_ylabel("True")
    plt.xticks(rotation=45, ha="right"); plt.tight_layout()
    path = f"{OUTPUT_DIR}/plots/{name.replace(' ','_')}_cm.png"
    fig.savefig(path, dpi=120); plt.close(fig)
    print(f"  Confusion matrix → {path}")

def plot_samples(xte, yt, yp, class_names, name):
    n = min(NUM_SAMPLES, len(xte))
    ncols = 4; nrows = int(np.ceil(n / ncols))
    fig = plt.figure(figsize=(ncols*3, nrows*3))
    fig.suptitle(f"Sample Predictions – {name}", fontweight="bold")
    for i in range(n):
        ax = fig.add_subplot(nrows, ncols, i+1)
        img = xte[i].squeeze()
        ax.imshow(img, cmap="gray" if xte[i].shape[-1]==1 else None)
        c = "#1B8B1B" if yt[i]==yp[i] else "#CC0000"
        ax.set_title(f"T:{class_names[yt[i]]}\nP:{class_names[yp[i]]}",
                     fontsize=7.5, color=c, fontweight="bold")
        ax.axis("off")
    plt.tight_layout()
    path = f"{OUTPUT_DIR}/plots/{name.replace(' ','_')}_samples.png"
    fig.savefig(path, dpi=120); plt.close(fig)
    print(f"  Sample predictions → {path}")

# ─────────────────────────────────────────────
# EVALUATE
# ─────────────────────────────────────────────
def evaluate(model, h, xte, yte, class_names, name, elapsed):
    loss, acc = model.evaluate(xte, yte, verbose=0)
    yp = np.argmax(model.predict(xte, verbose=0), axis=1)
    print(f"\n  {name}  |  Accuracy: {acc:.4f}  |  Loss: {loss:.4f}")
    print(classification_report(yte, yp, target_names=class_names))
    plot_history(h, name)
    plot_cm(yte, yp, class_names, name)
    plot_samples(xte, yte, yp, class_names, name)
    return {"name": name, "test_accuracy": round(acc,4),
            "test_loss": round(loss,4), "train_time_s": round(elapsed,1)}

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*55)
    print("  IMAGE CLASSIFICATION – QUICK TEST")
    print("  Dataset:", DATASET.upper(), "| Epochs:", EPOCHS)
    print("="*55)

    results = []

    # ── Basic CNN ─────────────────────────────────
    print("\n[1/3] Basic CNN")
    xtr, ytr, xval, yval, xte, yte, classes, shape = load_data(for_transfer=False)
    m1 = basic_cnn(shape, len(classes))
    h1, t1 = train(m1, xtr, ytr, xval, yval, f"{OUTPUT_DIR}/models/basic_cnn.keras")
    results.append(evaluate(m1, h1, xte, yte, classes, "Basic CNN", t1))

    # ── Improved CNN ──────────────────────────────
    print("\n[2/3] Improved CNN")
    m2 = improved_cnn(shape, len(classes))
    h2, t2 = train(m2, xtr, ytr, xval, yval, f"{OUTPUT_DIR}/models/improved_cnn.keras")
    results.append(evaluate(m2, h2, xte, yte, classes, "Improved CNN", t2))

    # ── Transfer Learning ─────────────────────────
    print("\n[3/3] Transfer Learning (MobileNetV2)")
    xtr_t, ytr_t, xval_t, yval_t, xte_t, yte_t, classes_t, shape_t = load_data(for_transfer=True)
    m3 = transfer_model(shape_t, len(classes_t))
    h3, t3 = train(m3, xtr_t, ytr_t, xval_t, yval_t, f"{OUTPUT_DIR}/models/transfer.keras")
    results.append(evaluate(m3, h3, xte_t, yte_t, classes_t, "Transfer MobileNetV2", t3))

    # ── Comparison ────────────────────────────────
    print("\n" + "="*55 + "\n  FINAL COMPARISON\n" + "="*55)
    df = pd.DataFrame([
        {"Model": r["name"], "Accuracy": r["test_accuracy"],
         "Loss": r["test_loss"], "Time(s)": r["train_time_s"]}
        for r in results
    ])
    print(df.to_string(index=False))
    best = max(results, key=lambda r: r["test_accuracy"])
    print(f"\n  🏆 Best: {best['name']}  ({best['test_accuracy']:.4f})")
    print(f"  Outputs saved to ./{OUTPUT_DIR}/\n")
