import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { api } from '../lib/api';

const SkeletonDraft = () => (
  <div className="space-y-4 animate-pulse">
    <div>
      <div className="h-4 bg-sage/20 rounded w-16 mb-2"></div>
      <div className="h-12 bg-cream-darker/30 rounded w-full"></div>
    </div>
    <div>
      <div className="h-4 bg-sage/20 rounded w-20 mb-2"></div>
      <div className="h-64 bg-cream-darker/30 rounded w-full"></div>
    </div>
  </div>
);

const OutreachDraft = ({ report, investor }) => {
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [copied, setCopied] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!report || !investor) return;
    setLoading(true);
    api.generateOutreachDraft(report, investor)
      .then(data => {
        setSubject(data.subject);
        setBody(data.body);
        setError(null);
      })
      .catch(err => setError(err.message || "Something didn't load right — try again in a moment."))
      .finally(() => setLoading(false));
  }, [report, investor]);

  const handleCopy = () => {
    navigator.clipboard.writeText(`Subject: ${subject}\n\n${body}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!investor) return null;

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white p-6 md:p-8 rounded-[var(--radius)] shadow-sm border border-sage/20"
    >
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-serif text-charcoal">Outreach Draft</h2>
          <p className="text-sm text-charcoal-muted mt-1">For {investor.name} at {investor.firm}</p>
        </div>
        <button 
          onClick={handleCopy}
          disabled={loading || error}
          className="text-sm font-medium bg-sage text-white px-4 py-2 rounded hover:bg-opacity-90 transition-all active:scale-95 disabled:opacity-50"
        >
          {copied ? "Copied!" : "Copy to Clipboard"}
        </button>
      </div>

      {error && !loading && (
        <div className="text-red-500 font-sans p-4 bg-red-50 rounded mb-4">
          {error}
        </div>
      )}

      {loading && <SkeletonDraft />}

      {!loading && !error && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-charcoal-muted mb-1">Subject</label>
            <input 
              type="text" 
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              className="w-full p-3 border border-gray-200 rounded text-charcoal focus:outline-none focus:border-sage focus:ring-1 focus:ring-sage font-sans transition-colors"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-charcoal-muted mb-1">Message</label>
            <textarea 
              value={body}
              onChange={(e) => setBody(e.target.value)}
              className="w-full min-h-[250px] p-4 border border-gray-200 rounded text-charcoal focus:outline-none focus:border-sage focus:ring-1 focus:ring-sage font-sans resize-y transition-colors leading-relaxed"
            />
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default OutreachDraft;
