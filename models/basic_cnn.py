"""
models/basic_cnn.py
-------------------
Baseline CNN model.

A simple, deliberately shallow network that serves as the
performance floor to beat with the improved and transfer-learning
models.
"""

from tensorflow.keras import layers, models


def build_basic_cnn(input_shape, num_classes):
    """
    Build and return a basic CNN model.

    Architecture
    ------------
    Conv2D(32) → ReLU → MaxPool
    Conv2D(64) → ReLU → MaxPool
    Flatten
    Dense(128) → ReLU
    Dense(num_classes) → Softmax

    Parameters
    ----------
    input_shape : tuple  e.g. (28, 28, 1)
    num_classes : int    number of output classes

    Returns
    -------
    tf.keras.Model (uncompiled)
    """
    model = models.Sequential(name="Basic_CNN")

    # ── Block 1 ──────────────────────────────────────────────
    model.add(layers.Conv2D(
        filters=32,
        kernel_size=(3, 3),
        activation="relu",
        padding="same",
        input_shape=input_shape,
        name="conv1"
    ))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), name="pool1"))

    # ── Block 2 ──────────────────────────────────────────────
    model.add(layers.Conv2D(
        filters=64,
        kernel_size=(3, 3),
        activation="relu",
        padding="same",
        name="conv2"
    ))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), name="pool2"))

    # ── Classifier head ──────────────────────────────────────
    model.add(layers.Flatten(name="flatten"))
    model.add(layers.Dense(128, activation="relu", name="fc1"))
    model.add(layers.Dense(num_classes, activation="softmax", name="output"))

    return model
