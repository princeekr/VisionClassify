"""
utils/evaluation.py
-------------------
Evaluation helpers: test-set metrics, confusion matrix,
classification report, sample predictions, and final comparison table.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import classification_report

from utils.visualization import (
    plot_training_history,
    plot_confusion_matrix,
    plot_sample_predictions,
    plot_model_comparison,
)


# ──────────────────────────────────────────────────────────────
# Single-model evaluation
# ──────────────────────────────────────────────────────────────

def evaluate_model(model, history, data, model_name, train_time_s=0.0):
    """
    Evaluate a trained model on the test set and produce all plots/reports.

    Parameters
    ----------
    model        : trained tf.keras.Model
    history      : tf.keras.callbacks.History
    data         : dict returned by load_dataset()
    model_name   : str  label used in titles / filenames
    train_time_s : float  total training wall-clock time in seconds

    Returns
    -------
    dict with keys: name, test_accuracy, test_loss, train_time_s
    """
    print(f"\n{'─'*55}")
    print(f"  Evaluating : {model_name}")
    print(f"{'─'*55}")

    x_test, y_test = data["x_test"], data["y_test"]
    class_names    = data["class_names"]

    # ── Test metrics ──────────────────────────────────────────
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"  Test Accuracy : {test_acc:.4f}  ({test_acc*100:.2f}%)")
    print(f"  Test Loss     : {test_loss:.4f}")

    # ── Predictions ───────────────────────────────────────────
    y_prob = model.predict(x_test, verbose=0)   # shape (N, num_classes)
    y_pred = np.argmax(y_prob, axis=1)

    # ── Classification report ────────────────────────────────
    print("\n  Classification Report:")
    print(classification_report(y_test, y_pred, target_names=class_names))

    # ── Plots ────────────────────────────────────────────────
    plot_training_history(history, model_name)
    plot_confusion_matrix(y_test, y_pred, class_names, model_name)
    plot_sample_predictions(x_test, y_test, y_pred, class_names, model_name)

    mins, secs = divmod(int(train_time_s), 60)
    print(f"  Training time : {mins}m {secs}s")

    return {
        "name":          model_name,
        "test_accuracy": round(test_acc, 4),
        "test_loss":     round(test_loss, 4),
        "train_time_s":  round(train_time_s, 1),
    }


# ──────────────────────────────────────────────────────────────
# Final comparison across all models
# ──────────────────────────────────────────────────────────────

def print_comparison_table(results):
    """
    Print a formatted comparison table and generate a bar chart.

    Parameters
    ----------
    results : list of dict (each returned by evaluate_model())
    """
    print(f"\n{'═'*65}")
    print("  FINAL MODEL COMPARISON")
    print(f"{'═'*65}")

    # Build a pandas DataFrame for pretty printing
    rows = []
    for r in results:
        mins, secs = divmod(int(r["train_time_s"]), 60)
        rows.append({
            "Model":         r["name"],
            "Test Accuracy": f"{r['test_accuracy']:.4f}",
            "Test Loss":     f"{r['test_loss']:.4f}",
            "Training Time": f"{mins}m {secs}s",
        })
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))

    # Best model
    best = max(results, key=lambda r: r["test_accuracy"])
    print(f"\n  🏆  Best model: {best['name']}  "
          f"(Test Accuracy = {best['test_accuracy']:.4f})")
    print(f"{'═'*65}\n")

    # Visual comparison chart
    plot_model_comparison(results)
