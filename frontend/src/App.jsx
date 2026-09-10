import React, { useState } from 'react';
import Card from './components/Card';
import AgentReveal from './components/AgentReveal';
import ReadinessScore from './components/ReadinessScore';
import MarketChart from './components/MarketChart';
import CompetitorList from './components/CompetitorList';
import RiskRadar from './components/RiskRadar';
import GlossaryTooltip from './components/GlossaryTooltip';
import { motion, AnimatePresence } from 'framer-motion';

// Mock Data
const MOCK_RESULTS = {
  marketSizeFinding: "Total Addressable Market is estimated at $12B globally, with a $1.5B SOM.",
  competitorFinding: "Found 3 close competitors; 2 successful exits and 1 failure due to execution.",
  riskFinding: "High execution risk, moderate market risk. Regulatory risk is minimal.",
  score: 78,
  scoreSummary: "Strong potential, but execution will be the primary challenge.",
  marketData: [
    { name: 'TAM', value: 12000 },
    { name: 'SAM', value: 4500 },
    { name: 'SOM', value: 1500 }
  ],
  competitors: [
    { name: 'Acme Corp', outcome: 'success', summary: 'Acquired for $200M after capturing 15% of the US market.', sourceLink: '#' },
    { name: 'Beta Inc', outcome: 'failure', summary: 'Failed to find product-market fit, burned $5M in funding.', sourceLink: '#' }
  ],
  riskData: [
    { subject: 'Market', value: 65 },
    { subject: 'Execution', value: 85 },
    { subject: 'Funding', value: 40 },
    { subject: 'Regulatory', value: 20 }
  ]
};

function App() {
  const [idea, setIdea] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [revealComplete, setRevealComplete] = useState(false);
  const [results, setResults] = useState(null);

  const handleAnalyze = () => {
    if (!idea.trim()) return;
    setIsAnalyzing(true);
    setRevealComplete(false);
    
    // Simulate API call
    setTimeout(() => {
      setResults(MOCK_RESULTS);
    }, 1000);
  };

  return (
    <div className="min-h-screen p-6 md:p-12 flex flex-col items-center">
      <div className="w-full max-w-5xl space-y-12 md:space-y-16 mt-4 md:mt-8">
        <header className="text-center space-y-4">
          <h1 className="text-4xl md:text-5xl font-medium text-sage tracking-tight">AI Co-Founder</h1>
          <p className="text-charcoal-muted text-lg md:text-xl font-light tracking-wide">
            Startup Idea Validation Platform
          </p>
        </header>

        <main className="space-y-12">
          {!isAnalyzing && !results && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
              <Card>
                <div className="flex flex-col gap-6">
                  <label htmlFor="idea" className="text-xl md:text-2xl font-serif text-charcoal">
                    What are you building?
                  </label>
                  <textarea 
                    id="idea"
                    className="w-full min-h-[180px] p-4 text-lg bg-transparent border border-gray-200 rounded-xl focus:outline-none focus:border-sage focus:ring-1 focus:ring-sage resize-none transition-colors"
                    placeholder="Describe your startup idea or current business situation in plain text..."
                    value={idea}
                    onChange={(e) => setIdea(e.target.value)}
                  />
                  <div className="flex justify-end mt-2">
                    <button 
                      onClick={handleAnalyze}
                      className="w-full md:w-auto bg-sage text-white px-8 py-3 min-h-[44px] rounded-[var(--radius)] font-medium text-lg hover:shadow-md hover:bg-opacity-95 transition-all duration-300 active:scale-[0.98]"
                    >
                      Analyze Idea
                    </button>
                  </div>
                </div>
              </Card>
            </motion.div>
          )}

          {isAnalyzing && (
            <AgentReveal 
              results={results} 
              onComplete={() => setRevealComplete(true)} 
            />
          )}

          <AnimatePresence>
            {revealComplete && results && (
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                className="space-y-8"
              >
                <div className="flex justify-between items-center">
                  <h2 className="text-3xl font-serif text-charcoal">Validation Report</h2>
                  <button 
                    onClick={() => {
                      setIsAnalyzing(false);
                      setResults(null);
                      setRevealComplete(false);
                      setIdea('');
                    }}
                    className="text-sage hover:text-sage-light transition-colors font-medium"
                  >
                    Start Over
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <ReadinessScore score={results.score} summary={results.scoreSummary} />
                  <RiskRadar data={results.riskData} />
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <MarketChart data={results.marketData} />
                  <CompetitorList competitors={results.competitors} />
                </div>

                <div className="bg-white p-8 rounded-[var(--radius)] shadow-sm">
                  <h3 className="text-xl font-serif text-charcoal mb-4">Synthesis</h3>
                  <p className="text-charcoal-muted leading-relaxed font-sans">
                    The total addressable market is large, but to effectively capture the <GlossaryTooltip term="SOM" definition="Serviceable Obtainable Market: the portion of the market you can realistically capture.">Serviceable Obtainable Market</GlossaryTooltip>, you will need a strong go-to-market strategy. Based on similar startups, the primary <GlossaryTooltip term="Execution Risk" definition="The risk that a company will not be able to execute its business plan effectively.">execution risk</GlossaryTooltip> lies in customer acquisition costs. Ensure you validate distribution channels early.
                  </p>
                </div>

              </motion.div>
            )}
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
}

export default App;
