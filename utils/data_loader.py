"""
utils/data_loader.py
--------------------
Handles dataset loading, preprocessing, validation splitting,
and on-the-fly resizing / grayscale-to-RGB conversion needed
for transfer learning.
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras import datasets

import config


# ──────────────────────────────────────────────────────────────
# Internal helpers
# ──────────────────────────────────────────────────────────────

def _get_class_names():
    """Return class names for the configured dataset."""
    if config.DATASET == "fashion_mnist":
        return config.FASHION_MNIST_CLASSES
    elif config.DATASET == "cifar10":
        return config.CIFAR10_CLASSES
    else:
        raise ValueError(f"Unknown dataset: {config.DATASET}. "
                         "Choose 'fashion_mnist' or 'cifar10'.")


def _load_raw():
    """Download (or use cached) dataset and return raw numpy arrays."""
    if config.DATASET == "fashion_mnist":
        (x_train, y_train), (x_test, y_test) = datasets.fashion_mnist.load_data()
    elif config.DATASET == "cifar10":
        (x_train, y_train), (x_test, y_test) = datasets.cifar10.load_data()
        # CIFAR-10 labels come as shape (N,1) – flatten to (N,)
        y_train = y_train.flatten()
        y_test  = y_test.flatten()
    return x_train, y_train, x_test, y_test


def _add_channel_dim(x):
    """
    Ensure images have an explicit channel dimension.
    Fashion-MNIST images are (N, 28, 28); we need (N, 28, 28, 1).
    CIFAR-10 images already have shape (N, 32, 32, 3).
    """
    if x.ndim == 3:          # grayscale without channel axis
        x = x[..., np.newaxis]
    return x


def _normalize(x):
    """Scale pixel values to [0, 1]."""
    return x.astype("float32") / 255.0


def _validation_split(x_train, y_train, val_fraction):
    """
    Randomly split training data into train / validation sets.
    Uses config.RANDOM_SEED for reproducibility.
    """
    np.random.seed(config.RANDOM_SEED)
    n = len(x_train)
    indices = np.random.permutation(n)
    val_size = int(n * val_fraction)
    val_idx   = indices[:val_size]
    train_idx = indices[val_size:]
    return (x_train[train_idx], y_train[train_idx],
            x_train[val_idx],   y_train[val_idx])


# ──────────────────────────────────────────────────────────────
# Resize helper used by transfer-learning pipeline
# ──────────────────────────────────────────────────────────────

def _resize_and_to_rgb(x, target_hw):
    """
    Resize a batch of images to target_hw=(H, W) and convert
    single-channel images to 3-channel RGB by tiling the channel.

    Parameters
    ----------
    x        : np.ndarray, shape (N, H_in, W_in, C_in)
    target_hw: tuple (H_out, W_out)

    Returns
    -------
    np.ndarray, shape (N, H_out, W_out, 3), dtype float32
    """
    h, w = target_hw
    # tf.image.resize works on float tensors
    x_tensor = tf.constant(x, dtype=tf.float32)
    x_resized = tf.image.resize(x_tensor, [h, w]).numpy()  # (N, h, w, C)

    # Convert grayscale → RGB
    if x_resized.shape[-1] == 1:
        x_resized = np.concatenate([x_resized] * 3, axis=-1)  # (N, h, w, 3)

    return x_resized


# ──────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────

def load_dataset(for_transfer_learning=False):
    """
    Load, preprocess and split the dataset configured in config.py.

    Parameters
    ----------
    for_transfer_learning : bool
        If True, images are resized to config.TRANSFER_IMAGE_SIZE
        and converted to 3-channel RGB (required by MobileNetV2 etc.).

    Returns
    -------
    dict with keys:
        x_train, y_train  – training split
        x_val,   y_val    – validation split
        x_test,  y_test   – test split
        class_names       – list of string labels
        num_classes       – int
        input_shape       – tuple (H, W, C)
    """
    print(f"\n{'='*55}")
    print(f"  Loading dataset : {config.DATASET.upper()}")
    if for_transfer_learning:
        target = config.TRANSFER_IMAGE_SIZE
        print(f"  Mode            : Transfer Learning (resize → {target})")
    else:
        print(f"  Mode            : Standard CNN")
    print(f"{'='*55}")

    # 1. Raw data
    x_train_raw, y_train_raw, x_test_raw, y_test_raw = _load_raw()

    # 2. Add channel dimension + normalise
    x_train_raw = _normalize(_add_channel_dim(x_train_raw))
    x_test_raw  = _normalize(_add_channel_dim(x_test_raw))

    # 3. Validation split (on raw training data, before any resize)
    x_train, y_train, x_val, y_val = _validation_split(
        x_train_raw, y_train_raw, config.VALIDATION_SPLIT
    )

    # 4. Optional resize + RGB conversion
    if for_transfer_learning:
        h, w, _ = config.TRANSFER_IMAGE_SIZE
        print("  Resizing images for transfer learning "
              f"({h}×{w}×3) – this may take a moment …")
        x_train = _resize_and_to_rgb(x_train, (h, w))
        x_val   = _resize_and_to_rgb(x_val,   (h, w))
        x_test  = _resize_and_to_rgb(x_test_raw,  (h, w))
        input_shape = (h, w, 3)
    else:
        x_test      = x_test_raw
        input_shape = x_train.shape[1:]   # (H, W, C)

    class_names = _get_class_names()
    num_classes = len(class_names)

    # 5. Summary
    print(f"\n  x_train : {x_train.shape}   y_train : {y_train.shape}")
    print(f"  x_val   : {x_val.shape}   y_val   : {y_val.shape}")
    print(f"  x_test  : {x_test.shape}   y_test  : {y_test_raw.shape}")
    print(f"  Classes : {num_classes}   Input shape : {input_shape}")
    print(f"{'='*55}\n")

    return {
        "x_train":     x_train,
        "y_train":     y_train,
        "x_val":       x_val,
        "y_val":       y_val,
        "x_test":      x_test,
        "y_test":      y_test_raw,
        "class_names": class_names,
        "num_classes": num_classes,
        "input_shape": input_shape,
    }
