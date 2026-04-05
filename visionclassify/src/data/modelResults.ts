/**
 * Centralized training results from the CNN project.
 * These values come from the actual trained models on Fashion-MNIST.
 *
 * Update these after re-training with different epochs / hyperparameters.
 */

export interface ModelResult {
  id: string;
  name: string;
  accuracy: string;
  accuracyNum: number;
  loss: string;
  time: string;
  notes: string;
  isWinner?: boolean;
}

export const MODEL_RESULTS: ModelResult[] = [
  {
    id: "basic",
    name: "Basic CNN",
    accuracy: "88.42%",
    accuracyNum: 88.42,
    loss: "0.3384",
    time: "1m 12s",
    notes: "Baseline model. 2 Conv layers + Dense head. Simple and fast to train.",
  },
  {
    id: "improved",
    name: "Improved CNN",
    accuracy: "89.25%",
    accuracyNum: 89.25,
    loss: "0.3012",
    time: "4m 30s",
    notes: "Added Dropout, Batch Normalization & Data Augmentation. Better generalization.",
  },
  {
    id: "transfer",
    name: "Transfer Learning (MobileNetV2)",
    accuracy: "89.79%",
    accuracyNum: 89.79,
    loss: "0.2973",
    time: "8m 45s",
    notes: "Pre-trained on ImageNet. Frozen base + custom head. Best performance.",
    isWinner: true,
  },
];

export const DATASET_INFO = {
  name: "Fashion-MNIST",
  totalImages: "70,000",
  imageSize: "28×28 pixels (Grayscale)",
  classes: 10,
  classNames: [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot",
  ],
  trainSize: "54,000 Training / 6,000 Validation / 10,000 Testing",
};

export const BEST_MODEL = MODEL_RESULTS.find((m) => m.isWinner)!;

/** Recharts-compatible data for the bar chart */
export const comparisonChartData = MODEL_RESULTS.map((m) => ({
  name: m.id === "transfer" ? "Transfer Learning" : m.name,
  accuracy: m.accuracyNum,
}));

/** Paths to output images (served from public/) */
export const PLOT_PATHS = {
  modelComparison: "/outputs/plots/model_comparison.png",
  trainingHistory: {
    basic: "/outputs/plots/Basic_CNN_training_history.png",
    improved: "/outputs/plots/Improved_CNN_training_history.png",
    transfer: "/outputs/plots/Transfer_Learning_(MobileNetV2)_training_history.png",
  },
  confusionMatrix: {
    basic: "/outputs/confusion_matrices/Basic_CNN_confusion_matrix.png",
    improved: "/outputs/confusion_matrices/Improved_CNN_confusion_matrix.png",
    transfer: "/outputs/confusion_matrices/Transfer_Learning_(MobileNetV2)_confusion_matrix.png",
  },
  samplePredictions: {
    basic: "/outputs/sample_predictions/Basic_CNN_sample_predictions.png",
    improved: "/outputs/sample_predictions/Improved_CNN_sample_predictions.png",
    transfer: "/outputs/sample_predictions/Transfer_Learning_(MobileNetV2)_sample_predictions.png",
  },
} as const;
