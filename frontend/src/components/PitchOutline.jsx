import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { api } from '../lib/api';

const PitchSection = ({ title, content, delay }) => (
  <motion.div 
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5, delay }}
    className="border-l-2 border-sage pl-6 py-2"
  >
    <h3 className="text-sm font-semibold tracking-wider text-sage uppercase mb-2">{title}</h3>
    <p className="text-charcoal-muted text-lg leading-relaxed font-sans">{content}</p>
  </motion.div>
);

const SkeletonSection = () => (
  <div className="border-l-2 border-sage/30 pl-6 py-2 animate-pulse mb-8">
    <div className="h-4 bg-sage/20 rounded w-24 mb-4"></div>
    <div className="space-y-2">
      <div className="h-5 bg-cream-darker rounded w-full"></div>
      <div className="h-5 bg-cream-darker rounded w-5/6"></div>
      <div className="h-5 bg-cream-darker rounded w-4/6"></div>
    </div>
  </div>
);

const PitchOutline = ({ report }) => {
  const [pitch, setPitch] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!report) return;
    setLoading(true);
    api.generatePitchOutline(report)
      .then(data => {
        setPitch(data);
        setError(null);
      })
      .catch(err => setError(err.message || "Something didn't load right — try again in a moment."))
      .finally(() => setLoading(false));
  }, [report]);

  return (
    <div className="bg-white p-8 md:p-12 rounded-[var(--radius)] shadow-sm">
      <h2 className="text-3xl font-serif text-charcoal mb-8">Pitch Outline</h2>
      
      {loading && (
        <div>
          <SkeletonSection />
          <SkeletonSection />
          <SkeletonSection />
        </div>
      )}

      {error && !loading && (
        <div className="text-red-500 font-sans p-4 bg-red-50 rounded">
          {error}
        </div>
      )}

      {pitch && !loading && (
        <div className="space-y-8">
          <PitchSection title="The Problem" content={pitch.problem} delay={0.1} />
          <PitchSection title="Our Solution" content={pitch.solution} delay={0.2} />
          <PitchSection title="The Market" content={pitch.market_size} delay={0.3} />
          <PitchSection title="Our Edge" content={pitch.competitive_edge} delay={0.4} />
          <PitchSection title="The Ask" content={pitch.ask} delay={0.5} />
        </div>
      )}
    </div>
  );
};

export default PitchOutline;
