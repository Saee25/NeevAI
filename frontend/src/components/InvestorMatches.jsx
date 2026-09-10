import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { api } from '../lib/api';

const SkeletonInvestor = () => (
  <div className="bg-white p-6 rounded-[var(--radius)] shadow-sm border border-gray-100 flex flex-col h-full animate-pulse">
    <div className="mb-4">
      <div className="h-6 bg-sage/20 rounded w-1/2 mb-2"></div>
      <div className="h-4 bg-sage/10 rounded w-1/3"></div>
    </div>
    <div className="flex-grow space-y-2 mt-4">
      <div className="h-4 bg-cream-darker/60 rounded w-full"></div>
      <div className="h-4 bg-cream-darker/60 rounded w-5/6"></div>
      <div className="h-4 bg-cream-darker/60 rounded w-4/6"></div>
    </div>
  </div>
);

const InvestorMatches = ({ report, onSelectInvestor, selectedInvestor }) => {
  const [investors, setInvestors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!report) return;
    setLoading(true);
    api.generateInvestorMatches(report)
      .then(data => {
        setInvestors(data);
        setError(null);
      })
      .catch(err => setError(err.message || "Something didn't load right — try again in a moment."))
      .finally(() => setLoading(false));
  }, [report]);

  return (
    <div className="space-y-6">
      <div className="bg-orange-50 text-orange-800 px-4 py-3 rounded-lg text-sm flex items-center gap-3">
        <span className="text-lg">⚠️</span>
        <p>Sample match — verify their current thesis and fund status before reaching out.</p>
      </div>

      <h2 className="text-2xl font-serif text-charcoal">Potential Investors</h2>

      {error && !loading && (
        <div className="text-red-500 font-sans p-4 bg-red-50 rounded">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading && (
          <>
            <SkeletonInvestor />
            <SkeletonInvestor />
            <SkeletonInvestor />
          </>
        )}

        {!loading && investors.map((inv, idx) => (
          <motion.div 
            key={idx}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4, delay: idx * 0.1 }}
            onClick={() => onSelectInvestor(inv)}
            className={`bg-white p-6 rounded-[var(--radius)] shadow-sm hover:shadow-md transition-all border cursor-pointer flex flex-col h-full ${
              selectedInvestor === inv ? 'border-sage ring-1 ring-sage' : 'border-gray-100 hover:border-sage/30'
            }`}
          >
            <div className="mb-4">
              <h3 className="text-xl font-medium text-charcoal">{inv.name}</h3>
              <p className="text-sage text-sm font-medium">{inv.firm}</p>
              <p className="text-xs text-charcoal-muted mt-1">{inv.stage} • {inv.sector}</p>
            </div>
            <div className="flex-grow">
              <p className="text-charcoal-muted text-sm leading-relaxed mb-4">{inv.description}</p>
              <div className="bg-cream-light p-3 rounded text-sm text-charcoal font-medium border border-cream-darker">
                <span className="text-sage font-bold mr-2">Why fit?</span> 
                {inv.match_reason}
              </div>
            </div>
            {selectedInvestor !== inv && (
              <div className="mt-4 text-sage text-sm font-medium opacity-0 hover:opacity-100 transition-opacity flex justify-end">
                Draft Outreach →
              </div>
            )}
          </motion.div>
        ))}
      </div>
      
      {!loading && investors.length === 0 && !error && (
        <div className="text-charcoal-muted p-4">No matching investors found.</div>
      )}
    </div>
  );
};

export default InvestorMatches;
