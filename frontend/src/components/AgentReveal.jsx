import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const steps = [
  { id: 'market', label: 'Checking market size...', getFinding: (r) => r.marketSizeFinding },
  { id: 'competitors', label: 'Scanning similar startups...', getFinding: (r) => r.competitorFinding },
  { id: 'risk', label: 'Assessing risk...', getFinding: (r) => r.riskFinding },
  { id: 'report', label: 'Synthesizing report...', getFinding: () => 'Final report generated successfully.' }
];

export default function AgentReveal({ results, onComplete }) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  useEffect(() => {
    if (!results) return;
    
    if (currentStepIndex < steps.length) {
      const timer = setTimeout(() => {
        setCurrentStepIndex(prev => prev + 1);
      }, 1500); // 1.5s per step
      return () => clearTimeout(timer);
    } else {
      if (onComplete) onComplete();
    }
  }, [currentStepIndex, results, onComplete]);

  if (!results) return null;

  return (
    <div className="w-full max-w-2xl mx-auto p-6 space-y-4">
      {steps.map((step, index) => {
        const isComplete = currentStepIndex > index;
        const isActive = currentStepIndex === index;
        const isPending = currentStepIndex < index;

        if (isPending && !isActive) return null;

        return (
          <motion.div
            key={step.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: "easeOut" }}
            className="flex flex-col gap-2"
          >
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 flex-shrink-0 flex items-center justify-center">
                {isComplete ? (
                  <svg className="w-6 h-6 text-sage" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                ) : (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
                    className="w-5 h-5 border-2 border-sage border-t-transparent rounded-full"
                  />
                )}
              </div>
              <span className={`text-lg font-serif ${isComplete ? 'text-charcoal' : 'text-sage'}`}>
                {step.label}
              </span>
            </div>
            
            <AnimatePresence>
              {isComplete && step.getFinding(results) && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  className="pl-9 text-charcoal-muted text-sm font-sans"
                >
                  {step.getFinding(results)}
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        );
      })}
    </div>
  );
}
