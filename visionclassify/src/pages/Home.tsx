import { motion } from "motion/react";
import { ArrowRight, BarChart3, Brain, Cpu, Layers } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts";
import { cn } from "@/lib/utils";
import { MODEL_RESULTS, BEST_MODEL, comparisonChartData } from "@/data/modelResults";

export function Home() {
  const basic = MODEL_RESULTS[0];
  const improved = MODEL_RESULTS[1];
  const transfer = MODEL_RESULTS[2];

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center max-w-3xl mx-auto pt-12 pb-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium mb-6 border border-primary/20">
            <span className="flex h-2 w-2 rounded-full bg-primary"></span>
            Academic Project Demo
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-foreground tracking-tight mb-6 leading-tight">
            Image Classification using <br className="hidden md:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-teal-500">
              CNN and Transfer Learning
            </span>
          </h1>
          <p className="text-lg text-muted-foreground mb-8 leading-relaxed">
            A deep learning system that classifies fashion images using custom CNN architectures and state-of-the-art transfer learning models.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button asChild size="lg" className="w-full sm:w-auto group">
              <Link to="/models">
                Explore Results
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg" className="w-full sm:w-auto">
              <Link to="/demo">Try Live Prediction</Link>
            </Button>
          </div>
        </motion.div>
      </section>

      {/* Metrics Cards */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Basic CNN"
          value={basic.accuracy}
          description="Test Accuracy"
          icon={<Cpu className="h-5 w-5 text-muted-foreground" />}
          delay={0.1}
        />
        <MetricCard
          title="Improved CNN"
          value={improved.accuracy}
          description="Test Accuracy"
          icon={<Layers className="h-5 w-5 text-muted-foreground" />}
          delay={0.2}
        />
        <MetricCard
          title="Transfer Learning"
          value={transfer.accuracy}
          description="Test Accuracy"
          icon={<Brain className="h-5 w-5 text-primary" />}
          highlight
          delay={0.3}
        />
        <MetricCard
          title="Dataset"
          value="Fashion-MNIST"
          description="10 Classes • 70k Images"
          icon={<BarChart3 className="h-5 w-5 text-muted-foreground" />}
          delay={0.4}
        />
      </section>

      {/* Overview & Chart Section */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="lg:col-span-2"
        >
          <Card className="h-full">
            <CardHeader>
              <CardTitle>Model Performance Comparison</CardTitle>
              <CardDescription>Test accuracy across different architectures</CardDescription>
            </CardHeader>
            <CardContent className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={comparisonChartData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                  <XAxis dataKey="name" stroke="currentColor" className="text-muted-foreground" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="currentColor" className="text-muted-foreground" fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
                  <Tooltip
                    cursor={{ fill: 'var(--color-muted)' }}
                    contentStyle={{ borderRadius: '8px', border: '1px solid var(--color-border)', backgroundColor: 'var(--color-card)', color: 'var(--color-card-foreground)', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  />
                  <Bar dataKey="accuracy" fill="var(--color-primary)" radius={[4, 4, 0, 0]} maxBarSize={60} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
        >
          <Card className="h-full bg-gradient-to-br from-primary to-purple-600 text-white border-none shadow-lg">
            <CardHeader>
              <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-white/20 text-white text-xs font-semibold w-fit mb-2">
                Best Model
              </div>
              <CardTitle className="text-white text-2xl">{BEST_MODEL.name}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-white/80 text-sm leading-relaxed">
                By leveraging pre-trained weights from ImageNet, the Transfer Learning model achieved the best classification accuracy on the Fashion-MNIST dataset with minimal training time.
              </p>
              <div className="pt-4 border-t border-white/20">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-white/80 text-sm">Accuracy</span>
                  <span className="font-bold">{BEST_MODEL.accuracy}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white/80 text-sm">Loss</span>
                  <span className="font-bold">{BEST_MODEL.loss}</span>
                </div>
              </div>
              <Button asChild variant="secondary" className="w-full mt-4 bg-white text-primary hover:bg-white/90">
                <Link to="/models">View Details</Link>
              </Button>
            </CardContent>
          </Card>
        </motion.div>
      </section>
    </div>
  );
}

function MetricCard({ title, value, description, icon, highlight = false, delay = 0 }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
    >
      <Card className={cn("h-full transition-shadow hover:shadow-md", highlight && "ring-2 ring-primary/20 bg-primary/5")}>
        <CardContent className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-medium text-muted-foreground">{title}</h3>
            {icon}
          </div>
          <div className="text-3xl font-bold text-foreground mb-1">{value}</div>
          <p className="text-xs text-muted-foreground">{description}</p>
        </CardContent>
      </Card>
    </motion.div>
  );
}
