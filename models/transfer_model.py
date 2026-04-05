"""
models/transfer_model.py
------------------------
Transfer learning model using MobileNetV2 pre-trained on ImageNet.

Two-stage strategy:
  Stage 1 – Feature extraction: freeze the entire base, train only
             the custom classification head.
  Stage 2 – Fine-tuning (optional): unfreeze the top N layers of the
             base and continue training with a very low learning rate.
"""

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

import config


def build_transfer_model(input_shape, num_classes, fine_tune=False, fine_tune_at=100):
    """
    Build and return a MobileNetV2-based transfer learning model.

    Parameters
    ----------
    input_shape  : tuple  e.g. (96, 96, 3)  – must be ≥ (32, 32, 3)
    num_classes  : int    number of output classes
    fine_tune    : bool   if True, unfreeze layers from fine_tune_at onwards
    fine_tune_at : int    layer index from which to start unfreezing

    Returns
    -------
    tf.keras.Model (uncompiled)
    """
    # ── Validate input ───────────────────────────────────────
    h, w, c = input_shape
    if c != 3:
        raise ValueError(
            f"MobileNetV2 requires 3-channel (RGB) input. "
            f"Received input_shape={input_shape}. "
            f"Use for_transfer_learning=True in load_dataset()."
        )
    if h < 32 or w < 32:
        raise ValueError(
            f"MobileNetV2 requires spatial dims ≥ 32×32. "
            f"Received {h}×{w}."
        )

    # ── Pre-trained base ──────────────────────────────────────
    base_model = MobileNetV2(
        input_shape=input_shape,
        include_top=False,        # remove ImageNet classification head
        weights="imagenet"
    )
    base_model.trainable = False  # freeze all layers initially

    # ── Optional fine-tuning: unfreeze top layers ─────────────
    if fine_tune:
        base_model.trainable = True
        for layer in base_model.layers[:fine_tune_at]:
            layer.trainable = False
        print(f"  [Transfer] Fine-tuning enabled: "
              f"layers {fine_tune_at}–{len(base_model.layers)} are trainable.")
    else:
        print("  [Transfer] Feature-extraction mode: base is fully frozen.")

    # ── Build the full model ──────────────────────────────────
    inputs = layers.Input(shape=input_shape, name="input")

    # MobileNetV2 expects pixel values in [-1, 1].
    # Our loader normalises to [0, 1], so we rescale here.
    x = layers.Rescaling(scale=2.0, offset=-1.0, name="mobilenet_preprocess")(inputs)

    # Base feature extractor (training=False keeps BN layers in inference
    # mode even when we fine-tune, which is the recommended practice)
    x = base_model(x, training=False)

    # ── Custom classification head ───────────────────────────
    x = layers.GlobalAveragePooling2D(name="gap")(x)
    x = layers.BatchNormalization(name="head_bn")(x)
    x = layers.Dense(256, activation="relu", name="head_fc1")(x)
    x = layers.Dropout(0.4, name="head_drop")(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="output")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="Transfer_MobileNetV2")
    return model


def unfreeze_for_fine_tuning(model, fine_tune_at=100, new_lr=None):
    """
    Unfreeze the MobileNetV2 base starting from `fine_tune_at` and
    recompile the model with a lower learning rate for fine-tuning.

    This function modifies the model **in place** and recompiles it.

    Parameters
    ----------
    model       : compiled tf.keras.Model
    fine_tune_at: int   layer index from which unfreezing starts
    new_lr      : float learning rate for fine-tuning
                  (defaults to config.FINE_TUNE_LR)
    """
    if new_lr is None:
        new_lr = config.FINE_TUNE_LR

    # The base model is the second layer of our functional model
    base_model = model.layers[2]          # index 0=input, 1=Rescaling, 2=base
    base_model.trainable = True

    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False

    n_trainable = sum(1 for l in base_model.layers if l.trainable)
    print(f"  [Fine-tune] {n_trainable} base layers unfrozen "
          f"(starting at layer {fine_tune_at}).")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=new_lr),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    print(f"  [Fine-tune] Model recompiled with lr={new_lr:.2e}")
    return model
