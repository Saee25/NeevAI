import React from 'react';

export default function CompetitorList({ competitors }) {
  return (
    <div className="bg-white p-6 rounded-[var(--radius)] shadow-sm w-full h-fit">
      <h3 className="text-xl font-serif text-charcoal mb-6">Similar Startups</h3>
      <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
        {competitors.map((comp, index) => (
          <div key={index} className="flex flex-col p-4 border border-gray-100 rounded-xl hover:shadow-sm transition-shadow">
            <div className="flex justify-between items-start mb-2">
              <h4 className="text-lg font-serif text-charcoal">{comp.name}</h4>
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${comp.outcome === 'success' ? 'bg-sage' : 'bg-red-400'}`} />
                <span className="text-xs text-charcoal-muted uppercase tracking-wider">{comp.outcome}</span>
              </div>
            </div>
            <p className="text-sm text-charcoal-muted mb-3 font-sans leading-relaxed">{comp.summary}</p>
            {comp.sourceLink && (
              <a 
                href={comp.sourceLink} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-xs text-sage hover:text-sage-light transition-colors font-medium self-start"
              >
                View Source &rarr;
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
