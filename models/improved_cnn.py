"""
models/improved_cnn.py
----------------------
Improved CNN model.

Adds Batch Normalization, Dropout, an extra convolutional block,
and (optionally) a data-augmentation preprocessing head.
These changes typically improve both accuracy and generalisation.
"""

from tensorflow.keras import layers, models


def build_improved_cnn(input_shape, num_classes, use_augmentation=True):
    """
    Build and return an improved CNN model.

    Architecture
    ------------
    [Optional augmentation layer]
    Conv2D(32) → BN → ReLU → Conv2D(32) → BN → ReLU → MaxPool → Dropout(0.25)
    Conv2D(64) → BN → ReLU → Conv2D(64) → BN → ReLU → MaxPool → Dropout(0.25)
    Conv2D(128)→ BN → ReLU                    → GlobalAvgPool → Dropout(0.4)
    Dense(256) → BN → ReLU → Dropout(0.5)
    Dense(num_classes) → Softmax

    Parameters
    ----------
    input_shape     : tuple  e.g. (28, 28, 1)
    num_classes     : int    number of output classes
    use_augmentation: bool   prepend random flip / rotate / zoom layers

    Returns
    -------
    tf.keras.Model (uncompiled)
    """
    inputs = layers.Input(shape=input_shape, name="input")
    x = inputs

    # ── Data augmentation (only active during training) ───────
    if use_augmentation:
        x = layers.RandomFlip("horizontal", name="aug_flip")(x)
        x = layers.RandomRotation(0.10, name="aug_rotate")(x)
        x = layers.RandomZoom(0.10, name="aug_zoom")(x)

    # ── Block 1 ───────────────────────────────────────────────
    x = layers.Conv2D(32, (3, 3), padding="same", use_bias=False, name="b1_conv1")(x)
    x = layers.BatchNormalization(name="b1_bn1")(x)
    x = layers.Activation("relu", name="b1_act1")(x)

    x = layers.Conv2D(32, (3, 3), padding="same", use_bias=False, name="b1_conv2")(x)
    x = layers.BatchNormalization(name="b1_bn2")(x)
    x = layers.Activation("relu", name="b1_act2")(x)

    x = layers.MaxPooling2D((2, 2), name="b1_pool")(x)
    x = layers.Dropout(0.25, name="b1_drop")(x)

    # ── Block 2 ───────────────────────────────────────────────
    x = layers.Conv2D(64, (3, 3), padding="same", use_bias=False, name="b2_conv1")(x)
    x = layers.BatchNormalization(name="b2_bn1")(x)
    x = layers.Activation("relu", name="b2_act1")(x)

    x = layers.Conv2D(64, (3, 3), padding="same", use_bias=False, name="b2_conv2")(x)
    x = layers.BatchNormalization(name="b2_bn2")(x)
    x = layers.Activation("relu", name="b2_act2")(x)

    x = layers.MaxPooling2D((2, 2), name="b2_pool")(x)
    x = layers.Dropout(0.25, name="b2_drop")(x)

    # ── Block 3 ───────────────────────────────────────────────
    x = layers.Conv2D(128, (3, 3), padding="same", use_bias=False, name="b3_conv1")(x)
    x = layers.BatchNormalization(name="b3_bn1")(x)
    x = layers.Activation("relu", name="b3_act1")(x)

    x = layers.GlobalAveragePooling2D(name="b3_gap")(x)
    x = layers.Dropout(0.4, name="b3_drop")(x)

    # ── Classifier head ──────────────────────────────────────
    x = layers.Dense(256, use_bias=False, name="fc1")(x)
    x = layers.BatchNormalization(name="fc1_bn")(x)
    x = layers.Activation("relu", name="fc1_act")(x)
    x = layers.Dropout(0.5, name="fc1_drop")(x)

    outputs = layers.Dense(num_classes, activation="softmax", name="output")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="Improved_CNN")
    return model
