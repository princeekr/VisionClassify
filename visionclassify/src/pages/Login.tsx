import React, { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Card, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { BrainCircuit, Loader2 } from "lucide-react";
import { Link, useNavigate, useLocation, Navigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";

export function Login() {
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [status, setStatus] = useState<'idle' | 'loading' | 'success'>('idle');

  const from = location.state?.from?.pathname || "/";

  if (isAuthenticated) {
    return <Navigate to={from} replace />;
  }

  const handleLogin = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setStatus('loading');

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 600));

    setStatus('success');

    // Wait for success animation to play out before redirecting
    setTimeout(() => {
      login();
      navigate(from, { replace: true });
    }, 2000);
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.2 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 24 } }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background relative overflow-hidden p-4">
      {/* Animated Background Elements */}
      <div className="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-primary/10 blur-[100px] mix-blend-normal animate-pulse pointer-events-none" style={{ animationDuration: '4s' }} />
      <div className="absolute bottom-[-10%] right-[-10%] w-[50vw] h-[50vw] rounded-full bg-blue-500/10 blur-[100px] mix-blend-normal animate-pulse pointer-events-none" style={{ animationDuration: '5s', animationDelay: '1s' }} />

      <div className="w-full max-w-md relative z-10">
        <AnimatePresence mode="wait">
          {status === 'success' ? (
            <motion.div
              key="success"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 1.1 }}
              className="flex flex-col items-center justify-center py-16 bg-card rounded-2xl border border-border/50 shadow-2xl"
            >
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", stiffness: 200, damping: 20, delay: 0.1 }}
                className="w-24 h-24 bg-emerald-500 rounded-full flex items-center justify-center shadow-lg shadow-emerald-500/30 mb-6"
              >
                <svg className="w-12 h-12 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                  <motion.path
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 0.5, delay: 0.3, ease: "easeOut" }}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </motion.div>
              <motion.h2
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="text-2xl font-bold text-foreground mb-2"
              >
                Login Successful
              </motion.h2>
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6 }}
                className="text-muted-foreground"
              >
                Redirecting to dashboard...
              </motion.p>
            </motion.div>
          ) : (
            <motion.div
              key="form"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
            >
              <div className="flex flex-col items-center mb-8">
                <motion.div
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ type: "spring", stiffness: 200, damping: 20 }}
                  className="bg-primary p-3 rounded-2xl text-primary-foreground mb-6 shadow-lg shadow-primary/25"
                >
                  <BrainCircuit size={36} />
                </motion.div>
                <motion.h1
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                  className="text-3xl font-bold text-foreground tracking-tight"
                >
                  Welcome back
                </motion.h1>
                <motion.p
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="text-muted-foreground text-sm mt-2"
                >
                  Sign in to your account to continue
                </motion.p>
              </div>

              <Card className="border-border/50 shadow-2xl bg-card/80 backdrop-blur-xl">
                <CardContent className="p-8">
                  <motion.form
                    variants={containerVariants}
                    initial="hidden"
                    animate="show"
                    className="space-y-5"
                    onSubmit={handleLogin}
                  >
                    <motion.div variants={itemVariants} className="space-y-2">
                      <label className="text-sm font-medium text-foreground" htmlFor="email">
                        Email
                      </label>
                      <input
                        id="email"
                        type="email"
                        placeholder="name@example.com"
                        className="w-full px-4 py-2.5 border border-border rounded-lg bg-background/50 text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
                        required
                      />
                    </motion.div>
                    <motion.div variants={itemVariants} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <label className="text-sm font-medium text-foreground" htmlFor="password">
                          Password
                        </label>
                        <a href="#" className="text-xs text-primary hover:underline font-medium">
                          Forgot password?
                        </a>
                      </div>
                      <input
                        id="password"
                        type="password"
                        placeholder="••••••••"
                        className="w-full px-4 py-2.5 border border-border rounded-lg bg-background/50 text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
                        required
                      />
                    </motion.div>
                    <motion.div variants={itemVariants} className="pt-2">
                      <Button type="submit" className="w-full py-6 text-base font-medium shadow-lg shadow-primary/20" disabled={status === 'loading'}>
                        {status === 'loading' ? (
                          <>
                            <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                            Signing in...
                          </>
                        ) : (
                          "Sign In"
                        )}
                      </Button>
                    </motion.div>

                    <motion.div variants={itemVariants} className="mt-6 flex items-center justify-center space-x-3">
                      <div className="h-px bg-border flex-1" />
                      <span className="text-xs text-muted-foreground uppercase tracking-wider font-semibold">Or continue with</span>
                      <div className="h-px bg-border flex-1" />
                    </motion.div>

                    <motion.div variants={itemVariants} className="mt-6">
                      <Button type="button" variant="outline" className="w-full py-6 flex items-center gap-3 bg-background/50 hover:bg-accent" onClick={() => handleLogin()} disabled={status === 'loading'}>
                        <svg viewBox="0 0 24 24" className="h-5 w-5" aria-hidden="true">
                          <path
                            d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                            fill="#4285F4"
                          />
                          <path
                            d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                            fill="#34A853"
                          />
                          <path
                            d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                            fill="#FBBC05"
                          />
                          <path
                            d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                            fill="#EA4335"
                          />
                        </svg>
                        <span className="font-medium">Google</span>
                      </Button>
                    </motion.div>
                    
                    <motion.p variants={itemVariants} className="mt-8 text-center text-sm text-muted-foreground">
                      Don't have an account?{" "}
                      <Link to="/login" className="text-primary font-semibold hover:underline">
                        Sign up
                      </Link>
                    </motion.p>
                  </motion.form>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
