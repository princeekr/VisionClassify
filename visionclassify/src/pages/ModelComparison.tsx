import { motion } from "motion/react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { Trophy } from "lucide-react";
import { MODEL_RESULTS, BEST_MODEL, PLOT_PATHS } from "@/data/modelResults";

export function ModelComparison() {
  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-foreground tracking-tight mb-2">Model Comparison</h1>
        <p className="text-muted-foreground">Side-by-side performance metrics of all trained architectures.</p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-muted-foreground uppercase bg-muted/50 border-b border-border">
                <tr>
                  <th className="px-6 py-4 font-medium">Model Name</th>
                  <th className="px-6 py-4 font-medium">Accuracy</th>
                  <th className="px-6 py-4 font-medium">Loss</th>
                  <th className="px-6 py-4 font-medium">Training Time</th>
                  <th className="px-6 py-4 font-medium">Notes / Strengths</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {MODEL_RESULTS.map((model) => (
                  <tr
                    key={model.name}
                    className={model.isWinner ? "bg-primary/5" : "hover:bg-muted/50 transition-colors"}
                  >
                    <td className="px-6 py-4 font-medium text-foreground flex items-center gap-2">
                      {model.name}
                      {model.isWinner && <Trophy size={16} className="text-primary" />}
                    </td>
                    <td className="px-6 py-4">
                      <span className={model.isWinner ? "text-primary font-semibold" : "text-foreground/80"}>
                        {model.accuracy}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-muted-foreground">{model.loss}</td>
                    <td className="px-6 py-4 text-muted-foreground">{model.time}</td>
                    <td className="px-6 py-4 text-muted-foreground">{model.notes}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="lg:col-span-2"
        >
          <Card className="h-full">
            <CardHeader>
              <CardTitle>Visual Comparison</CardTitle>
              <CardDescription>Bar chart representation of model accuracies</CardDescription>
            </CardHeader>
            <CardContent className="flex items-center justify-center p-6">
              <img
                src={PLOT_PATHS.modelComparison}
                alt="Model comparison bar chart"
                className="w-full rounded-lg border border-border"
              />
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <Card className="h-full border-primary/20 bg-primary/5">
            <CardHeader>
              <div className="flex items-center gap-2 mb-2">
                <Trophy className="h-5 w-5 text-primary" />
                <span className="text-sm font-semibold text-primary uppercase tracking-wider">Winner</span>
              </div>
              <CardTitle className="text-xl">Transfer Learning</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-muted-foreground text-sm leading-relaxed">
              <p>
                The Transfer Learning model utilizing a pre-trained MobileNetV2 architecture emerged as the clear winner.
              </p>
              <p>
                <strong className="text-foreground">Why it won:</strong>
              </p>
              <ul className="list-disc pl-5 space-y-1">
                <li>Leveraged rich feature representations learned from millions of images on ImageNet.</li>
                <li>Lightweight architecture (MobileNetV2) suitable for laptop training with just a custom classification head.</li>
                <li>Achieved {BEST_MODEL.accuracy} accuracy with minimal overfitting, confirming the power of transfer learning.</li>
              </ul>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
