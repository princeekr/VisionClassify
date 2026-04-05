"""
utils/visualization.py
-----------------------
All plotting utilities.  Every plot is saved to disk automatically.
"""

import os

import matplotlib
matplotlib.use("Agg")          # non-interactive backend (safe for all systems)
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix

import config

# Make sure output directories exist when this module is imported
for _d in [config.PLOTS_DIR, config.CONFUSION_DIR, config.PREDICTIONS_DIR]:
    os.makedirs(_d, exist_ok=True)


# ──────────────────────────────────────────────────────────────
# Training curves
# ──────────────────────────────────────────────────────────────

def plot_training_history(history, model_name):
    """
    Plot and save accuracy + loss curves (train vs validation).

    Parameters
    ----------
    history    : tf.keras.callbacks.History
    model_name : str  used in the title and filename
    """
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(f"Training History – {model_name}", fontsize=14, fontweight="bold")

    # ── Accuracy ─────────────────────────────────────────────
    ax = axes[0]
    ax.plot(history.history["accuracy"],     label="Train Accuracy",      color="#2196F3")
    ax.plot(history.history["val_accuracy"], label="Validation Accuracy", color="#FF9800",
            linestyle="--")
    ax.set_title("Accuracy")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Accuracy")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # ── Loss ─────────────────────────────────────────────────
    ax = axes[1]
    ax.plot(history.history["loss"],     label="Train Loss",      color="#4CAF50")
    ax.plot(history.history["val_loss"], label="Validation Loss", color="#F44336",
            linestyle="--")
    ax.set_title("Loss")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    safe_name = model_name.replace(" ", "_").replace("/", "_")
    save_path = os.path.join(config.PLOTS_DIR, f"{safe_name}_training_history.png")
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [Plot] Training history saved → {save_path}")


# ──────────────────────────────────────────────────────────────
# Confusion matrix
# ──────────────────────────────────────────────────────────────

def plot_confusion_matrix(y_true, y_pred, class_names, model_name):
    """
    Compute and save a normalised confusion matrix heatmap.

    Parameters
    ----------
    y_true      : array-like of int
    y_pred      : array-like of int
    class_names : list of str
    model_name  : str
    """
    cm = confusion_matrix(y_true, y_pred)
    cm_norm = cm.astype("float") / cm.sum(axis=1, keepdims=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        cm_norm,
        annot=True,
        fmt=".2f",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
        ax=ax,
        linewidths=0.5
    )
    ax.set_title(f"Confusion Matrix – {model_name}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Predicted Label", fontsize=11)
    ax.set_ylabel("True Label",      fontsize=11)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()

    safe_name = model_name.replace(" ", "_").replace("/", "_")
    save_path = os.path.join(config.CONFUSION_DIR, f"{safe_name}_confusion_matrix.png")
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [Plot] Confusion matrix saved → {save_path}")


# ──────────────────────────────────────────────────────────────
# Sample predictions grid
# ──────────────────────────────────────────────────────────────

def plot_sample_predictions(x_test, y_true, y_pred, class_names, model_name,
                            n_samples=None):
    """
    Display a grid of test images with their true and predicted labels.
    Correct predictions are framed green; wrong ones red.

    Parameters
    ----------
    x_test      : np.ndarray  (N, H, W, C)
    y_true      : array-like of int
    y_pred      : array-like of int
    class_names : list of str
    model_name  : str
    n_samples   : int | None  defaults to config.NUM_SAMPLE_PREDICTIONS
    """
    if n_samples is None:
        n_samples = config.NUM_SAMPLE_PREDICTIONS

    # Take the first n_samples images for reproducibility
    indices = np.arange(min(n_samples, len(x_test)))
    n_cols  = 4
    n_rows  = int(np.ceil(len(indices) / n_cols))

    fig = plt.figure(figsize=(n_cols * 3, n_rows * 3.2))
    fig.suptitle(f"Sample Predictions – {model_name}", fontsize=13, fontweight="bold",
                 y=1.01)

    for i, idx in enumerate(indices):
        ax = fig.add_subplot(n_rows, n_cols, i + 1)

        img = x_test[idx]
        # Squeeze channel dim for display if grayscale
        display_img = img.squeeze() if img.shape[-1] == 1 else img
        cmap = "gray" if img.shape[-1] == 1 else None
        ax.imshow(display_img, cmap=cmap)

        true_label = class_names[int(y_true[idx])]
        pred_label = class_names[int(y_pred[idx])]
        correct    = (y_true[idx] == y_pred[idx])

        color      = "#1B8B1B" if correct else "#CC0000"
        ax.set_title(f"T: {true_label}\nP: {pred_label}",
                     fontsize=7.5, color=color, fontweight="bold")
        ax.axis("off")

        # Colour border
        for spine in ax.spines.values():
            spine.set_edgecolor(color)
            spine.set_linewidth(2.5)

    plt.tight_layout()
    safe_name = model_name.replace(" ", "_").replace("/", "_")
    save_path = os.path.join(config.PREDICTIONS_DIR,
                             f"{safe_name}_sample_predictions.png")
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [Plot] Sample predictions saved → {save_path}")


# ──────────────────────────────────────────────────────────────
# Comparison bar chart
# ──────────────────────────────────────────────────────────────

def plot_model_comparison(results):
    """
    Create a grouped bar chart comparing test accuracy across models.

    Parameters
    ----------
    results : list of dict, each with keys
                'name', 'test_accuracy', 'test_loss', 'train_time_s'
    """
    names     = [r["name"]          for r in results]
    accs      = [r["test_accuracy"] for r in results]
    losses    = [r["test_loss"]     for r in results]

    x     = np.arange(len(names))
    width = 0.35
    colors_acc  = ["#2196F3", "#4CAF50", "#FF9800"]
    colors_loss = ["#90CAF9", "#A5D6A7", "#FFCC80"]

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()

    bars1 = ax1.bar(x - width/2, accs,   width, color=colors_acc,  label="Test Accuracy",
                    alpha=0.9, zorder=3)
    bars2 = ax2.bar(x + width/2, losses, width, color=colors_loss, label="Test Loss",
                    alpha=0.9, zorder=3)

    # Annotate accuracy values on bars
    for bar, acc in zip(bars1, accs):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.002,
                 f"{acc:.4f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax1.set_ylabel("Test Accuracy", fontsize=11)
    ax2.set_ylabel("Test Loss",     fontsize=11)
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, fontsize=11)
    ax1.set_title("Model Comparison – Test Accuracy & Loss",
                  fontsize=13, fontweight="bold")
    ax1.set_ylim(0, 1.05)
    ax1.grid(axis="y", alpha=0.3, zorder=0)

    # Combined legend
    lines = [bars1, bars2]
    labels = ["Test Accuracy", "Test Loss"]
    ax1.legend(lines, labels, loc="lower right")

    plt.tight_layout()
    save_path = os.path.join(config.PLOTS_DIR, "model_comparison.png")
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [Plot] Model comparison chart saved → {save_path}")
