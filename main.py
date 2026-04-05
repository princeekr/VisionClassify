"""
main.py
-------
Entry point for the Image Classification project.

Run with:
    python main.py

This script trains three models sequentially:
  1. Basic CNN
  2. Improved CNN
  3. Transfer Learning (MobileNetV2)

…then compares their performance and saves all outputs.
"""

import os
import sys
import random
import warnings

# ── Suppress verbose TF/CUDA info messages ────────────────────
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
warnings.filterwarnings("ignore")

import numpy as np
import tensorflow as tf

# ── Project imports ───────────────────────────────────────────
import config
from utils.data_loader   import load_dataset
from utils.train_utils   import train_model
from utils.evaluation    import evaluate_model, print_comparison_table

from models.basic_cnn      import build_basic_cnn
from models.improved_cnn   import build_improved_cnn
from models.transfer_model import build_transfer_model


# ──────────────────────────────────────────────────────────────
# Reproducibility
# ──────────────────────────────────────────────────────────────
def set_seeds(seed=config.RANDOM_SEED):
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)


# ──────────────────────────────────────────────────────────────
# Ensure output directories exist
# ──────────────────────────────────────────────────────────────
def make_output_dirs():
    for d in [config.PLOTS_DIR, config.CONFUSION_DIR,
              config.PREDICTIONS_DIR, config.SAVED_MODELS_DIR]:
        os.makedirs(d, exist_ok=True)


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────
def main():
    set_seeds()
    make_output_dirs()

    print("\n" + "═" * 60)
    print("  IMAGE CLASSIFICATION – CNN & TRANSFER LEARNING")
    print("  Dataset :", config.DATASET.upper())
    print("  Device  :", "GPU" if tf.config.list_physical_devices("GPU") else "CPU")
    print("═" * 60)

    results = []   # accumulates evaluation dicts

    # ══════════════════════════════════════════════════════════
    # 1. BASIC CNN
    # ══════════════════════════════════════════════════════════
    data_std = load_dataset(for_transfer_learning=False)

    basic_model = build_basic_cnn(
        input_shape=data_std["input_shape"],
        num_classes=data_std["num_classes"]
    )
    history_basic, time_basic = train_model(
        basic_model, data_std,
        model_save_path=config.BASIC_MODEL_PATH,
        model_name="Basic CNN"
    )
    result_basic = evaluate_model(
        basic_model, history_basic, data_std,
        model_name="Basic CNN",
        train_time_s=time_basic
    )
    results.append(result_basic)

    # ══════════════════════════════════════════════════════════
    # 2. IMPROVED CNN
    # ══════════════════════════════════════════════════════════
    improved_model = build_improved_cnn(
        input_shape=data_std["input_shape"],
        num_classes=data_std["num_classes"],
        use_augmentation=True
    )
    history_improved, time_improved = train_model(
        improved_model, data_std,
        model_save_path=config.IMPROVED_MODEL_PATH,
        model_name="Improved CNN"
    )
    result_improved = evaluate_model(
        improved_model, history_improved, data_std,
        model_name="Improved CNN",
        train_time_s=time_improved
    )
    results.append(result_improved)

    # ══════════════════════════════════════════════════════════
    # 3. TRANSFER LEARNING (MobileNetV2)
    # ══════════════════════════════════════════════════════════
    # Transfer learning needs larger, 3-channel images
    data_tl = load_dataset(for_transfer_learning=True)

    transfer_model = build_transfer_model(
        input_shape=data_tl["input_shape"],
        num_classes=data_tl["num_classes"],
        fine_tune=False          # Stage 1: frozen base
    )
    history_transfer, time_transfer = train_model(
        transfer_model, data_tl,
        model_save_path=config.TRANSFER_MODEL_PATH,
        model_name="Transfer Learning (MobileNetV2)"
    )
    result_transfer = evaluate_model(
        transfer_model, history_transfer, data_tl,
        model_name="Transfer Learning (MobileNetV2)",
        train_time_s=time_transfer
    )
    results.append(result_transfer)

    # ══════════════════════════════════════════════════════════
    # COMPARISON
    # ══════════════════════════════════════════════════════════
    print_comparison_table(results)

    print("  All outputs saved to: ./outputs/")
    print("  ✔ Project complete!\n")


if __name__ == "__main__":
    main()
