/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider } from "./components/theme-provider";
import { AuthProvider } from "./contexts/AuthContext";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { Layout } from "./components/layout/Layout";
import { Home } from "./pages/Home";
import { ModelComparison } from "./pages/ModelComparison";
import { TrainingResults } from "./pages/TrainingResults";
import { ConfusionMatrices } from "./pages/ConfusionMatrices";
import { SamplePredictions } from "./pages/SamplePredictions";
import { LivePrediction } from "./pages/LivePrediction";
import { About } from "./pages/About";
import { Login } from "./pages/Login";

export default function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="visionclassify-theme">
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
              <Route index element={<Home />} />
              <Route path="models" element={<ModelComparison />} />
              <Route path="training" element={<TrainingResults />} />
              <Route path="confusion-matrix" element={<ConfusionMatrices />} />
              <Route path="samples" element={<SamplePredictions />} />
              <Route path="demo" element={<LivePrediction />} />
              <Route path="about" element={<About />} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}
