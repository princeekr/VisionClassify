import { motion } from "motion/react";
import { Card } from "@/components/ui/Card";
import { PLOT_PATHS } from "@/data/modelResults";

const matrices = [
  {
    id: "basic",
    title: "Basic CNN",
    description: "Struggles with visually similar classes like Pullover, Coat, and Shirt. The off-diagonal noise highlights where the basic architecture falls short without regularization.",
  },
  {
    id: "improved",
    title: "Improved CNN",
    description: "Better overall diagonal intensity thanks to Batch Normalization and Dropout. Some confusion between Shirt and T-shirt/top remains, but generalization is improved.",
  },
  {
    id: "transfer",
    title: "Transfer Learning (MobileNetV2)",
    description: "Strongest diagonal with minimal off-diagonal noise. The pre-trained features from ImageNet provide excellent class discrimination across almost all categories.",
  },
];

export function ConfusionMatrices() {
  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-foreground tracking-tight mb-2">Confusion Matrices</h1>
        <p className="text-muted-foreground">Visualizing class-wise performance and common misclassifications.</p>
      </motion.div>

      <div className="grid grid-cols-1 gap-8">
        {matrices.map((matrix, idx) => (
          <motion.div
            key={matrix.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: idx * 0.1 }}
          >
            <Card className="overflow-hidden">
              <div className="grid grid-cols-1 md:grid-cols-3">
                <div className="p-6 md:col-span-1 bg-muted/30 border-b md:border-b-0 md:border-r border-border flex flex-col justify-center">
                  <h3 className="text-xl font-semibold text-foreground mb-2">{matrix.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{matrix.description}</p>
                </div>
                <div className="p-6 md:col-span-2 flex items-center justify-center bg-card">
                  <img
                    src={PLOT_PATHS.confusionMatrix[matrix.id as keyof typeof PLOT_PATHS.confusionMatrix]}
                    alt={`${matrix.title} confusion matrix`}
                    className="w-full max-w-lg rounded-lg border border-border"
                  />
                </div>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
