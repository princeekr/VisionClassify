import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { cn } from "@/lib/utils";
import { PLOT_PATHS } from "@/data/modelResults";

const models = [
  { id: "basic", name: "Basic CNN" },
  { id: "improved", name: "Improved CNN" },
  { id: "transfer", name: "Transfer Learning" },
];

export function TrainingResults() {
  const [activeTab, setActiveTab] = useState(models[0].id);

  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-foreground tracking-tight mb-2">Training Results</h1>
        <p className="text-muted-foreground">Learning curves showing accuracy and loss over epochs.</p>
      </motion.div>

      {/* Custom Tabs */}
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
                layoutId="active-tab"
                className="absolute inset-0 bg-background rounded-lg shadow-sm border border-border"
                transition={{ type: "spring", stiffness: 400, damping: 30 }}
              />
            )}
            <span className="relative z-10">{model.name}</span>
          </button>
        ))}
      </div>

      <div className="relative min-h-[500px]">
        <AnimatePresence mode="wait">
          {models.map(
            (model) =>
              activeTab === model.id && (
                <motion.div
                  key={model.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-6"
                >
                  <Card>
                    <CardHeader>
                      <CardTitle>Training History – {model.name}</CardTitle>
                      <CardDescription>Accuracy and loss curves (training vs validation) across epochs</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <img
                        src={PLOT_PATHS.trainingHistory[model.id as keyof typeof PLOT_PATHS.trainingHistory]}
                        alt={`${model.name} training history`}
                        className="w-full rounded-lg border border-border"
                      />
                    </CardContent>
                  </Card>

                  <Card className="bg-primary/5 border-primary/20">
                    <CardContent className="p-6">
                      <h4 className="font-semibold text-primary mb-2">Analysis</h4>
                      <p className="text-sm text-foreground/80 leading-relaxed">
                        {model.id === "basic" && "The Basic CNN shows signs of overfitting after several epochs, as the training accuracy continues to rise while validation accuracy plateaus. The gap between training and validation loss widens towards the end, which is expected for a model lacking regularization."}
                        {model.id === "improved" && "With the addition of Dropout, Batch Normalization, and Data Augmentation, the Improved CNN generalizes much better. The validation curves track the training curves more closely, indicating reduced overfitting. The augmentation layers introduce controlled noise that helps the model learn more robust features."}
                        {model.id === "transfer" && "The Transfer Learning model (MobileNetV2) converges rapidly within the first few epochs thanks to its pre-trained ImageNet weights. Both accuracy and loss curves show excellent generalization, with validation metrics remaining close to training metrics. The frozen base layers act as a powerful feature extractor right from the start."}
                      </p>
                    </CardContent>
                  </Card>
                </motion.div>
              )
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
