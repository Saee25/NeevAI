import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { api } from '../lib/api';

const SkeletonAdvice = () => (
  <div className="space-y-6 animate-pulse">
    <div className="bg-white p-8 rounded-[var(--radius)] shadow-sm border-l-4 border-sage">
      <div className="h-6 bg-sage/20 rounded w-1/3 mb-4"></div>
      <div className="space-y-3 ml-6">
        <div className="h-4 bg-cream-darker/60 rounded w-full"></div>
        <div className="h-4 bg-cream-darker/60 rounded w-5/6"></div>
      </div>
    </div>
    <div className="bg-white p-8 rounded-[var(--radius)] shadow-sm border-l-4 border-red-400">
      <div className="h-6 bg-red-400/20 rounded w-1/3 mb-4"></div>
      <div className="space-y-3 ml-6">
        <div className="h-4 bg-cream-darker/60 rounded w-full"></div>
        <div className="h-4 bg-cream-darker/60 rounded w-4/6"></div>
      </div>
    </div>
  </div>
);

const ScalingAdvisor = ({ ideaText }) => {
  const [revenueContext, setRevenueContext] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!revenueContext.trim()) return;
    setIsAnalyzing(true);
    setError(null);
    try {
      const data = await api.getScalingAdvice(ideaText, revenueContext);
      setResult(data);
    } catch (err) {
      setError(err.message || "Something didn't load right — try again in a moment.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-8 mt-8">
      <div className="text-sm text-charcoal-muted mb-4 bg-gray-50 p-4 rounded-lg">
        <p><strong>Note:</strong> We provide qualitative, strategy-focused reasoning based on similar case studies. We will never invent specific numeric financial recommendations.</p>
      </div>

      {error && !isAnalyzing && (
        <div className="text-red-500 font-sans p-4 bg-red-50 rounded">
          {error}
        </div>
      )}

      {!result && !isAnalyzing && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="bg-white p-8 rounded-[var(--radius)] shadow-sm">
          <h2 className="text-2xl font-serif text-charcoal mb-4">Already have a business?</h2>
          <p className="text-charcoal-muted mb-6">Tell us about your current revenue context, growth channels, and challenges. We'll consult our case studies for scaling directions.</p>
          
          <textarea 
            className="w-full min-h-[150px] p-4 bg-transparent border border-gray-200 rounded-xl focus:outline-none focus:border-sage focus:ring-1 focus:ring-sage resize-none transition-colors mb-4 text-charcoal"
            placeholder="e.g., We are doing $10k MRR primarily through inbound content marketing, but growth has plateaued..."
            value={revenueContext}
            onChange={(e) => setRevenueContext(e.target.value)}
          />
          <div className="flex justify-end">
            <button 
              onClick={handleAnalyze}
              disabled={!revenueContext.trim()}
              className="bg-sage text-white px-6 py-2.5 rounded-[var(--radius)] font-medium hover:bg-opacity-95 transition-all active:scale-95 disabled:opacity-50"
            >
              Get Scaling Advice
            </button>
          </div>
        </motion.div>
      )}

      {isAnalyzing && <SkeletonAdvice />}

      {result && !isAnalyzing && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
          <div className="bg-white p-8 rounded-[var(--radius)] shadow-sm border-l-4 border-sage">
            <h3 className="text-xl font-medium text-charcoal mb-4 flex items-center gap-2">
              <span className="text-sage">✓</span> Feasible Directions
            </h3>
            <ul className="space-y-4">
              {result.feasible_directions?.map((item, i) => (
                <li key={i} className="text-charcoal-muted leading-relaxed ml-6 list-disc">
                  <span className="font-semibold text-charcoal block">{item.direction}</span>
                  {item.reasoning}
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-white p-8 rounded-[var(--radius)] shadow-sm border-l-4 border-red-400">
            <h3 className="text-xl font-medium text-charcoal mb-4 flex items-center gap-2">
              <span className="text-red-400">✗</span> Not Recommended
            </h3>
            <ul className="space-y-4">
              {result.not_recommended?.map((item, i) => (
                <li key={i} className="text-charcoal-muted leading-relaxed ml-6 list-disc">
                  <span className="font-semibold text-charcoal block">{item.direction}</span>
                  {item.reasoning}
                </li>
              ))}
            </ul>
          </div>
          
          <div className="flex justify-center pt-4">
             <button 
                onClick={() => { setResult(null); setRevenueContext(''); }}
                className="text-sage hover:text-sage-light font-medium"
             >
                Start Over
             </button>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default ScalingAdvisor;
