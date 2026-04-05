"""
utils/train_utils.py
--------------------
Reusable helpers for compiling, training, and saving models.
"""

import os
import time

import tensorflow as tf
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
)

import config


# ──────────────────────────────────────────────────────────────
# Compile
# ──────────────────────────────────────────────────────────────

def compile_model(model, learning_rate=None):
    """
    Compile a Keras model with Adam optimiser, sparse-categorical
    cross-entropy loss, and accuracy metric.

    Parameters
    ----------
    model         : tf.keras.Model (uncompiled)
    learning_rate : float | None  – defaults to config.LEARNING_RATE

    Returns
    -------
    compiled tf.keras.Model
    """
    if learning_rate is None:
        learning_rate = config.LEARNING_RATE

    model.compile(
        optimizer=optimizers.Adam(learning_rate=learning_rate),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model


# ──────────────────────────────────────────────────────────────
# Callbacks
# ──────────────────────────────────────────────────────────────

def get_callbacks(model_save_path):
    """
    Return a list of standard training callbacks.

    Includes:
    - EarlyStopping   – stops when val_loss stops improving
    - ModelCheckpoint – saves the best model weights
    - ReduceLROnPlateau – lowers LR when val_loss stagnates

    Parameters
    ----------
    model_save_path : str  full path where the best model is saved

    Returns
    -------
    list of tf.keras.callbacks.Callback
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)

    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=config.EARLY_STOPPING_PATIENCE,
        restore_best_weights=True,
        verbose=1
    )

    checkpoint = ModelCheckpoint(
        filepath=model_save_path,
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1
    )

    reduce_lr = ReduceLROnPlateau(
        monitor="val_loss",
        factor=config.REDUCE_LR_FACTOR,
        patience=config.REDUCE_LR_PATIENCE,
        min_lr=config.MIN_LR,
        verbose=1
    )

    return [early_stop, checkpoint, reduce_lr]


# ──────────────────────────────────────────────────────────────
# Train
# ──────────────────────────────────────────────────────────────

def train_model(model, data, model_save_path, model_name="Model"):
    """
    Compile, fit, and save the best checkpoint of a model.

    Parameters
    ----------
    model           : uncompiled tf.keras.Model
    data            : dict returned by load_dataset()
    model_save_path : str  path to save the best weights
    model_name      : str  label for console output

    Returns
    -------
    history : tf.keras.callbacks.History
    elapsed : float  wall-clock training time in seconds
    """
    print(f"\n{'─'*55}")
    print(f"  Training : {model_name}")
    print(f"{'─'*55}")
    model.summary(line_length=70)

    # Compile
    compile_model(model)

    callbacks = get_callbacks(model_save_path)

    start = time.time()
    history = model.fit(
        data["x_train"], data["y_train"],
        validation_data=(data["x_val"], data["y_val"]),
        epochs=config.EPOCHS,
        batch_size=config.BATCH_SIZE,
        callbacks=callbacks,
        verbose=1
    )
    elapsed = time.time() - start

    mins, secs = divmod(int(elapsed), 60)
    print(f"\n  ✔ {model_name} training complete – {mins}m {secs}s")
    print(f"  Best model saved to: {model_save_path}")

    return history, elapsed
