"""
server.py
---------
Lightweight Flask API that serves the best trained model for live prediction.

Run with:
    python server.py

Endpoints:
    POST /api/predict   – upload an image, get top-3 predictions
    GET  /api/model-info – return model metadata
"""

import os
import io
import warnings

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
warnings.filterwarnings("ignore")

import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS

import config

# ──────────────────────────────────────────────────────────────
# Setup
# ──────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)  # Allow requests from Vite dev server

CLASS_NAMES = config.CLASS_NAMES
MODEL_PATH = config.TRANSFER_MODEL_PATH  # best saved model
TRANSFER_SIZE = config.TRANSFER_IMAGE_SIZE[:2]  # (96, 96)

# ──────────────────────────────────────────────────────────────
# Load model once at startup
# ──────────────────────────────────────────────────────────────
print(f"  Loading model from: {MODEL_PATH}")
model = tf.keras.models.load_model(MODEL_PATH)
print(f"  Model loaded successfully: {model.name}")
print(f"  Input shape: {model.input_shape}")
print(f"  Classes: {CLASS_NAMES}")


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Preprocess an uploaded image for the transfer learning model.

    Steps:
    1. Open with PIL
    2. Convert to grayscale (Fashion-MNIST style)
    3. Resize to TRANSFER_SIZE (96×96)
    4. Normalize to [0, 1]
    5. Convert grayscale to 3-channel RGB
    6. Add batch dimension
    """
    img = Image.open(io.BytesIO(image_bytes))

    # Convert to grayscale first (model was trained on Fashion-MNIST grayscale)
    img = img.convert("L")

    # Resize to transfer learning size
    img = img.resize(TRANSFER_SIZE, Image.Resampling.LANCZOS)

    # Convert to numpy array and normalize
    arr = np.array(img, dtype=np.float32) / 255.0  # shape (96, 96)

    # Convert grayscale to 3-channel by tiling
    arr = np.stack([arr, arr, arr], axis=-1)  # shape (96, 96, 3)

    # Add batch dimension
    arr = np.expand_dims(arr, axis=0)  # shape (1, 96, 96, 3)

    return arr


# ──────────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────────

@app.route("/api/predict", methods=["POST"])
def predict():
    """Accept an image upload and return top-3 predictions."""
    if "image" not in request.files:
        return jsonify({"error": "No image file provided. Send as 'image' in multipart form."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename."}), 400

    try:
        image_bytes = file.read()
        processed = preprocess_image(image_bytes)

        # Run inference
        predictions = model.predict(processed, verbose=0)[0]  # shape (num_classes,)

        # Get top-3 predictions
        top3_indices = np.argsort(predictions)[::-1][:3]
        top3 = [
            {"label": CLASS_NAMES[int(i)], "score": round(float(predictions[i]) * 100, 1)}
            for i in top3_indices
        ]

        best_idx = int(top3_indices[0])
        result = {
            "class": CLASS_NAMES[best_idx],
            "confidence": round(float(predictions[best_idx]), 4),
            "model": "Transfer Learning (MobileNetV2)",
            "top3": top3,
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


@app.route("/api/model-info", methods=["GET"])
def model_info():
    """Return metadata about the loaded model."""
    return jsonify({
        "model_name": "Transfer Learning (MobileNetV2)",
        "dataset": config.DATASET,
        "num_classes": len(CLASS_NAMES),
        "class_names": CLASS_NAMES,
        "input_shape": list(model.input_shape[1:]),
        "total_params": int(model.count_params()),
    })


# ──────────────────────────────────────────────────────────────
# Run
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n  ╔══════════════════════════════════════════╗")
    print("  ║  VisionClassify API Server               ║")
    print("  ║  http://localhost:5000                    ║")
    print("  ╚══════════════════════════════════════════╝\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
