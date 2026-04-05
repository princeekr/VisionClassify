import { useState } from "react";
import { motion } from "motion/react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { cn } from "@/lib/utils";
import { PLOT_PATHS } from "@/data/modelResults";

const models = [
  { id: "basic", name: "Basic CNN" },
  { id: "improved", name: "Improved CNN" },
  { id: "transfer", name: "Transfer Learning (MobileNetV2)" },
];

export function SamplePredictions() {
  const [activeTab, setActiveTab] = useState(models[0].id);

  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-foreground tracking-tight mb-2">Sample Predictions</h1>
        <p className="text-muted-foreground">Real model predictions on test set images. Green = correct, Red = incorrect.</p>
      </motion.div>

      {/* Tabs */}
      <div className="flex space-x-1 bg-muted/50 p-1 rounded-xl w-fit border border-border">
        {models.map((model) => (
          <button
            key={model.id}
            onClick={() => setActiveTab(model.id)}
            className={cn(
              "relative px-4 py-2 text-sm font-medium rounded-lg transition-colors outline-none",
              activeTab === model.id ? "text-primary" : "text-muted-foreground hover:text-foreground hover:bg-muted"
            )}
          >
            {activeTab === model.id && (
              <motion.div
                layoutId="sample-tab"
                className="absolute inset-0 bg-background rounded-lg shadow-sm border border-border"
                transition={{ type: "spring", stiffness: 400, damping: 30 }}
              />
            )}
            <span className="relative z-10">{model.name}</span>
          </button>
        ))}
      </div>

      {/* Image */}
      {models.map(
        (model) =>
          activeTab === model.id && (
            <motion.div
              key={model.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle>Predictions – {model.name}</CardTitle>
                  <CardDescription>
                    A grid of test images with actual labels (T) and predicted labels (P).
                    Green titles indicate correct predictions, red indicates misclassifications.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <img
                    src={PLOT_PATHS.samplePredictions[model.id as keyof typeof PLOT_PATHS.samplePredictions]}
                    alt={`${model.name} sample predictions`}
                    className="w-full rounded-lg border border-border"
                  />
                </CardContent>
              </Card>
            </motion.div>
          )
      )}
    </div>
  );
}
