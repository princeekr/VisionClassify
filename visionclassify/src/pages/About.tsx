import { motion } from "motion/react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { BookOpen, Code2, Database, Layers } from "lucide-react";
import { BEST_MODEL, DATASET_INFO } from "@/data/modelResults";

export function About() {
  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center mb-12"
      >
        <h1 className="text-3xl font-bold text-foreground tracking-tight mb-4">Project Documentation</h1>
        <p className="text-muted-foreground text-lg">Technical details and academic abstract of the image classification system.</p>
      </motion.div>

      <div className="space-y-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }}>
          <Card>
            <CardHeader className="flex flex-row items-center gap-4 pb-2">
              <div className="p-2 bg-primary/10 rounded-lg text-primary">
                <BookOpen size={24} />
              </div>
              <CardTitle>Academic Abstract</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground leading-relaxed text-sm md:text-base">
                Image classification remains a foundational challenge in computer vision. This project explores and compares the efficacy of custom Convolutional Neural Networks (CNNs) against Transfer Learning techniques for classifying fashion apparel. Using the Fashion-MNIST dataset as a benchmark, we developed a baseline CNN, an improved CNN with regularization techniques (Batch Normalization, Dropout, Data Augmentation), and fine-tuned a pre-trained MobileNetV2 model. Our results demonstrate that while custom architectures can achieve commendable accuracy (&gt;88%), leveraging deep pre-trained networks via transfer learning yields superior generalization and accuracy ({BEST_MODEL.accuracy}), highlighting the power of feature reuse in modern deep learning paradigms.
              </p>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.2 }}>
          <Card>
            <CardHeader className="flex flex-row items-center gap-4 pb-2">
              <div className="p-2 bg-teal-500/10 rounded-lg text-teal-500">
                <Layers size={24} />
              </div>
              <CardTitle>Model Architecture</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <h4 className="font-semibold text-foreground mb-1">1. Basic CNN</h4>
                <p className="text-sm text-muted-foreground">A simple sequential model comprising 2 Convolutional layers (Conv2D → MaxPool) followed by a Flatten and Dense classification head. Serves as a baseline to understand fundamental feature extraction without any regularization.</p>
              </div>
              <div>
                <h4 className="font-semibold text-foreground mb-1">2. Improved CNN</h4>
                <p className="text-sm text-muted-foreground">Builds upon the basic architecture by introducing Batch Normalization after each Conv layer, Dropout (0.25–0.5) to prevent overfitting, and Data Augmentation (random flip, rotation, zoom). Uses GlobalAveragePooling instead of Flatten for a more parameter-efficient design.</p>
              </div>
              <div>
                <h4 className="font-semibold text-foreground mb-1">3. Transfer Learning (MobileNetV2)</h4>
                <p className="text-sm text-muted-foreground">Utilizes the MobileNetV2 architecture pre-trained on ImageNet (1.2M images, 1000 classes). The base model layers are frozen, and a custom classification head (GlobalAveragePooling → BatchNorm → Dense 256 → Dropout → Dense 10) is appended. Images are resized to 96×96 and converted from grayscale to 3-channel RGB for compatibility.</p>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.3 }}>
            <Card className="h-full">
              <CardHeader className="flex flex-row items-center gap-4 pb-2">
                <div className="p-2 bg-rose-500/10 rounded-lg text-rose-500">
                  <Database size={24} />
                </div>
                <CardTitle>Dataset Information</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li><strong className="text-foreground">Name:</strong> {DATASET_INFO.name}</li>
                  <li><strong className="text-foreground">Total Images:</strong> {DATASET_INFO.totalImages}</li>
                  <li><strong className="text-foreground">Image Size:</strong> {DATASET_INFO.imageSize}</li>
                  <li><strong className="text-foreground">Classes:</strong> {DATASET_INFO.classes} ({DATASET_INFO.classNames.join(", ")})</li>
                  <li><strong className="text-foreground">Split:</strong> {DATASET_INFO.trainSize}</li>
                </ul>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.4 }}>
            <Card className="h-full">
              <CardHeader className="flex flex-row items-center gap-4 pb-2">
                <div className="p-2 bg-blue-500/10 rounded-lg text-blue-500">
                  <Code2 size={24} />
                </div>
                <CardTitle>Tech Stack</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h5 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Machine Learning</h5>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-2.5 py-1 bg-muted text-foreground/80 text-xs rounded-md">Python</span>
                      <span className="px-2.5 py-1 bg-muted text-foreground/80 text-xs rounded-md">TensorFlow / Keras</span>
                      <span className="px-2.5 py-1 bg-muted text-foreground/80 text-xs rounded-md">NumPy</span>
                      <span className="px-2.5 py-1 bg-muted text-foreground/80 text-xs rounded-md">Matplotlib</span>
                      <span className="px-2.5 py-1 bg-muted text-foreground/80 text-xs rounded-md">Scikit-learn</span>
                    </div>
                  </div>
                  <div>
                    <h5 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Backend API</h5>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-2.5 py-1 bg-muted text-foreground/80 text-xs rounded-md">Flask</span>
                      <span className="px-2.5 py-1 bg-muted text-foreground/80 text-xs rounded-md">Pillow</span>
                    </div>
                  </div>
                  <div>
                    <h5 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Frontend / Dashboard</h5>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-2.5 py-1 bg-muted text-foreground/80 text-xs rounded-md">React 19</span>
                      <span className="px-2.5 py-1 bg-muted text-foreground/80 text-xs rounded-md">TypeScript</span>
                      <span className="px-2.5 py-1 bg-muted text-foreground/80 text-xs rounded-md">Tailwind CSS</span>
                      <span className="px-2.5 py-1 bg-muted text-foreground/80 text-xs rounded-md">Framer Motion</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
