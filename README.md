# Image Classification using CNN and Transfer Learning

> **Academic Deep Learning Project** – Python · TensorFlow/Keras · Fashion-MNIST

---

## Project Overview

This project implements and compares three image classification approaches:

1. **Basic CNN** – A lightweight convolutional network serving as a performance baseline.
2. **Improved CNN** – A deeper network with Batch Normalisation, Dropout, and Data Augmentation for better accuracy and generalisation.
3. **Transfer Learning (MobileNetV2)** – Fine-tuned ImageNet weights adapted to the target dataset, demonstrating state-of-the-art efficiency.

The project is structured as a real-world ML pipeline: modular code, automatic dataset loading, configurable hyperparameters, training callbacks, full evaluation metrics, and saved visualisations.

---

## Features

- Automatic dataset download via `tf.keras.datasets`
- Train / Validation / Test splits with a fixed random seed
- Three model architectures with increasing complexity
- EarlyStopping, ModelCheckpoint, ReduceLROnPlateau callbacks
- Confusion matrix, classification report, training curves
- Sample prediction grid (green = correct, red = wrong)
- Final comparison table + bar chart
- Easy switching between Fashion-MNIST and CIFAR-10 via `config.py`

---

## Dataset

| Property        | Fashion-MNIST (default)     | CIFAR-10              |
|-----------------|-----------------------------|-----------------------|
| Images          | 70 000 (60k train, 10k test)| 60 000 (50k/10k)      |
| Image size      | 28 × 28 grayscale           | 32 × 32 RGB           |
| Classes         | 10 clothing categories      | 10 object categories  |
| Source          | `tf.keras.datasets`         | `tf.keras.datasets`   |

To switch to CIFAR-10 open `config.py` and set:
```python
DATASET          = "cifar10"
NATIVE_IMAGE_SIZE = (32, 32, 3)
```

---

## Model Descriptions

### 1. Basic CNN (Baseline)
Two convolutional blocks (Conv → MaxPool) followed by a Dense head.  
No regularisation; intentionally simple so performance improvements are clearly visible.

### 2. Improved CNN
Three convolutional blocks with **Batch Normalisation** and **Dropout** per block, plus **Data Augmentation** (random flip, rotation, zoom) to reduce overfitting. Uses **GlobalAveragePooling** instead of Flatten for a smaller parameter count.

### 3. Transfer Learning – MobileNetV2
Pre-trained on ImageNet (1.2M images, 1 000 classes). The convolutional base is frozen; only a lightweight classification head is trained. Images are upscaled to 96×96 and converted to 3-channel RGB automatically.

---

## Typical Results (Fashion-MNIST, 25 epochs)

| Model | Test Accuracy | Test Loss |
|-------|--------------|-----------|
| Basic CNN | ~89% | ~0.31 |
| Improved CNN | ~91% | ~0.25 |
| Transfer Learning | ~92–93% | ~0.23 |

*Results vary slightly due to random weight initialisation.*

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: tensorflow` | Run `pip install -r requirements.txt` |
| Training very slow | Set `EPOCHS = 3` in `config.py`; use CPU is fine for Fashion-MNIST |
| `ResourceExhaustedError` (OOM) | Reduce `BATCH_SIZE` to 32 in `config.py` |
| Transfer model shape error | Ensure `for_transfer_learning=True` is used in `load_dataset()` – the main script handles this automatically |
| Plots not opening | Plots are saved to `outputs/` – open the `.png` files directly |
| `AttributeError: RandomFlip` | Update TensorFlow: `pip install --upgrade tensorflow` |

---

## Abstract

Deep learning has transformed computer vision by enabling automatic feature extraction from raw pixel data. This project investigates image classification on the Fashion-MNIST benchmark dataset through three progressively sophisticated architectures. A baseline Convolutional Neural Network (CNN) establishes a performance floor using standard convolutional and pooling layers. An enhanced variant introduces batch normalisation, dropout regularisation, and online data augmentation to improve generalisation. Finally, transfer learning via MobileNetV2—a lightweight architecture pre-trained on ImageNet—demonstrates how knowledge from large-scale datasets can be effectively adapted to domain-specific tasks with limited computational resources. Experimental results confirm that each successive approach yields measurable improvements in classification accuracy, validating the practical utility of regularisation and transfer learning techniques for real-world deep learning applications.

**Keywords:** Convolutional Neural Networks, Transfer Learning, MobileNetV2, Fashion-MNIST, Image Classification, TensorFlow, Keras.

---

*Project developed for – Deep Learning*
