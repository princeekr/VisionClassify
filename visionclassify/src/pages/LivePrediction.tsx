import React, { useState } from "react";
import { motion } from "motion/react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { UploadCloud, Image as ImageIcon, Loader2, RefreshCw } from "lucide-react";

export function LivePrediction() {
  const [isDragging, setIsDragging] = useState(false);
  const [image, setImage] = useState<string | null>(null);
  const [isPredicting, setIsPredicting] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFile = (file: File) => {
    setSelectedFile(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      setImage(e.target?.result as string);
      runPrediction(file);
    };
    reader.readAsDataURL(file);
  };

  const runPrediction = async (file: File) => {
    setIsPredicting(true);
    setResult(null);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("image", file);

      const response = await fetch("/api/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || "Server error");
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      console.error("Prediction error:", err);
      setError(
        err.message.includes("Failed to fetch")
          ? "Cannot reach the prediction server. Make sure to run: python server.py"
          : err.message
      );
    } finally {
      setIsPredicting(false);
    }
  };

  const reset = () => {
    setImage(null);
    setResult(null);
    setError(null);
    setSelectedFile(null);
  };

  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-foreground tracking-tight mb-2">Live Prediction</h1>
        <p className="text-muted-foreground">Upload an image to test the model in real-time.</p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Column: Upload Area */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <Card className="h-full">
            <CardHeader>
              <CardTitle>Input Image</CardTitle>
              <CardDescription>Upload a fashion item image (28×28 grayscale preferred)</CardDescription>
            </CardHeader>
            <CardContent>
              {!image ? (
                <div
                  className={`border-2 border-dashed rounded-xl p-12 text-center transition-colors ${
                    isDragging ? "border-primary bg-primary/5" : "border-border hover:border-primary/50 hover:bg-muted/50"
                  }`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                >
                  <UploadCloud className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                  <h3 className="text-sm font-semibold text-foreground mb-1">Drag & drop your image here</h3>
                  <p className="text-xs text-muted-foreground mb-4">PNG, JPG up to 5MB</p>
                  <div className="relative">
                    <Button variant="outline" size="sm">Browse Files</Button>
                    <input
                      type="file"
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      accept="image/*"
                      onChange={handleFileChange}
                    />
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="relative aspect-square max-w-sm mx-auto bg-muted rounded-xl overflow-hidden border border-border flex items-center justify-center">
                    <img src={image} alt="Uploaded" className="max-w-full max-h-full object-contain" />
                  </div>
                  <div className="flex justify-center">
                    <Button variant="ghost" size="sm" onClick={reset} className="text-muted-foreground">
                      <RefreshCw className="mr-2 h-4 w-4" />
                      Upload Another
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>

        {/* Right Column: Results */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Card className="h-full bg-muted/30">
            <CardHeader>
              <CardTitle>Prediction Results</CardTitle>
              <CardDescription>Inference output from the best saved model</CardDescription>
            </CardHeader>
            <CardContent>
              {!image ? (
                <div className="h-64 flex flex-col items-center justify-center text-muted-foreground space-y-4">
                  <ImageIcon className="h-12 w-12 opacity-20" />
                  <p className="text-sm">Upload an image to see results</p>
                </div>
              ) : isPredicting ? (
                <div className="h-64 flex flex-col items-center justify-center text-primary space-y-4">
                  <Loader2 className="h-8 w-8 animate-spin" />
                  <p className="text-sm font-medium animate-pulse">Running inference...</p>
                </div>
              ) : error ? (
                <div className="h-64 flex flex-col items-center justify-center text-rose-500 space-y-4">
                  <div className="p-4 bg-rose-500/10 rounded-xl border border-rose-500/20 max-w-sm text-center">
                    <p className="text-sm font-medium mb-2">Prediction Failed</p>
                    <p className="text-xs text-rose-400">{error}</p>
                  </div>
                </div>
              ) : result ? (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="space-y-6"
                >
                  <div className="p-6 bg-card rounded-xl border border-border shadow-sm text-center">
                    <p className="text-sm text-muted-foreground mb-1">Predicted Class</p>
                    <h2 className="text-3xl font-bold text-primary mb-2">{result.class}</h2>
                    <div className="inline-flex items-center px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs font-semibold">
                      {(result.confidence * 100).toFixed(1)}% Confidence
                    </div>
                  </div>

                  <div>
                    <h4 className="text-sm font-semibold text-foreground mb-4">Top Predictions</h4>
                    <div className="space-y-3">
                      {result.top3.map((item: any, idx: number) => (
                        <div key={idx} className="space-y-1">
                          <div className="flex justify-between text-sm">
                            <span className="text-foreground/80">{item.label}</span>
                            <span className="text-muted-foreground font-medium">{item.score}%</span>
                          </div>
                          <div className="h-2 w-full bg-muted rounded-full overflow-hidden">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${item.score}%` }}
                              transition={{ duration: 0.8, delay: 0.2 + idx * 0.1 }}
                              className={`h-full rounded-full ${idx === 0 ? "bg-primary" : "bg-muted-foreground/40"}`}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="pt-4 border-t border-border">
                    <p className="text-xs text-muted-foreground">
                      Model used: <span className="font-medium text-foreground/80">{result.model}</span>
                    </p>
                  </div>
                </motion.div>
              ) : null}
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
