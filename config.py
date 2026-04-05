"""
config.py
---------
Central configuration file for the Image Classification project.
Edit the values here to customize dataset, training, and paths.
"""

import os

# ─────────────────────────────────────────────
# DATASET SETTINGS
# ─────────────────────────────────────────────
# Choose between 'fashion_mnist' or 'cifar10'
# >>> CHANGE ONLY THIS LINE TO SWITCH DATASET <<<
DATASET = "fashion_mnist"

# Fraction of training data used for validation
VALIDATION_SPLIT = 0.1

# ─────────────────────────────────────────────
# CLASS NAMES
# ─────────────────────────────────────────────
FASHION_MNIST_CLASSES = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"
]

CIFAR10_CLASSES = [
    "Airplane", "Automobile", "Bird", "Cat", "Deer",
    "Dog", "Frog", "Horse", "Ship", "Truck"
]

# ─────────────────────────────────────────────
# IMAGE SETTINGS (auto-detected from DATASET)
# ─────────────────────────────────────────────
if DATASET == "fashion_mnist":
    NATIVE_IMAGE_SIZE = (28, 28, 1)
    CLASS_NAMES = FASHION_MNIST_CLASSES
elif DATASET == "cifar10":
    NATIVE_IMAGE_SIZE = (32, 32, 3)
    CLASS_NAMES = CIFAR10_CLASSES
else:
    raise ValueError(f"Unknown DATASET='{DATASET}'. Choose 'fashion_mnist' or 'cifar10'.")

NUM_CLASSES = len(CLASS_NAMES)

# Transfer learning models require larger, 3-channel images
TRANSFER_IMAGE_SIZE = (96, 96, 3)  # Upscale for MobileNetV2

# ─────────────────────────────────────────────
# TRAINING HYPERPARAMETERS
# ─────────────────────────────────────────────
BATCH_SIZE = 64
EPOCHS = 25           # Set to 3 for a quick smoke-test
LEARNING_RATE = 1e-3
FINE_TUNE_LR = 1e-5   # Used during transfer-learning fine-tuning

# ─────────────────────────────────────────────
# EARLY STOPPING & SCHEDULER
# ─────────────────────────────────────────────
EARLY_STOPPING_PATIENCE = 7
REDUCE_LR_PATIENCE = 3
REDUCE_LR_FACTOR = 0.5
MIN_LR = 1e-7

# ─────────────────────────────────────────────
# OUTPUT PATHS
# ─────────────────────────────────────────────
BASE_OUTPUT_DIR      = "outputs"
PLOTS_DIR            = os.path.join(BASE_OUTPUT_DIR, "plots")
CONFUSION_DIR        = os.path.join(BASE_OUTPUT_DIR, "confusion_matrices")
PREDICTIONS_DIR      = os.path.join(BASE_OUTPUT_DIR, "sample_predictions")
SAVED_MODELS_DIR     = os.path.join(BASE_OUTPUT_DIR, "saved_models")

BASIC_MODEL_PATH     = os.path.join(SAVED_MODELS_DIR, "basic_cnn_best.keras")
IMPROVED_MODEL_PATH  = os.path.join(SAVED_MODELS_DIR, "improved_cnn_best.keras")
TRANSFER_MODEL_PATH  = os.path.join(SAVED_MODELS_DIR, "transfer_model_best.keras")

# ─────────────────────────────────────────────
# MISC
# ─────────────────────────────────────────────
RANDOM_SEED = 42
NUM_SAMPLE_PREDICTIONS = 16   # How many test images to display in the grid
