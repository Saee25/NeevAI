import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const steps = [
  { 
    id: 'market', 
    label: 'Checking market size...', 
    getFinding: (r) => r?.marketReasoning ? `${r.marketReasoning.slice(0, 90)}...` : 'Market size calculated.' 
  },
  { 
    id: 'competitors', 
    label: 'Scanning similar startups...', 
    getFinding: (r) => r?.competitors?.length ? `Identified ${r.competitors.length} comparable startups.` : 'Competitive landscape analyzed.' 
  },
  { 
    id: 'risk', 
    label: 'Assessing risk...', 
    getFinding: (r) => r?.riskData?.length ? 'Risk profile calculated across 4 dimensions.' : 'Risk factors evaluated.' 
  },
  { 
    id: 'report', 
    label: 'Synthesizing report...', 
    getFinding: () => 'Final report generated successfully.' 
  }
];

export default function AgentReveal({ results, isAnalyzing, onComplete }) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  useEffect(() => {
    // Progress through earlier steps with timing
    if (currentStepIndex < steps.length - 1) {
      const timer = setTimeout(() => {
        setCurrentStepIndex(prev => prev + 1);
      }, 1500);
      return () => clearTimeout(timer);
    } else if (currentStepIndex === steps.length - 1) {
      // On the final step, complete once results have arrived
      if (results) {
        const timer = setTimeout(() => {
          setCurrentStepIndex(steps.length);
          if (onComplete) onComplete();
        }, 800);
        return () => clearTimeout(timer);
      }
    } else {
      if (onComplete) onComplete();
    }
  }, [currentStepIndex, results, onComplete]);

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
              {isComplete && results && step.getFinding(results) && (
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
