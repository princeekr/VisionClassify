import { BrainCircuit } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-border bg-background/50 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2 text-muted-foreground">
            <BrainCircuit size={18} />
            <span className="font-medium text-foreground">VisionClassify</span>
            <span className="text-sm border-l border-border pl-2 ml-1">Deep Learning</span>
          </div>
          <div className="text-sm text-muted-foreground">
            Image Classification &bull; {new Date().getFullYear()}
          </div>
        </div>
      </div>
    </footer>
  );
}
