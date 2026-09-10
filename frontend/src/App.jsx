import React, { useState } from 'react';
import Card from './components/Card';
import AgentReveal from './components/AgentReveal';
import ReadinessScore from './components/ReadinessScore';
import MarketChart from './components/MarketChart';
import CompetitorList from './components/CompetitorList';
import RiskRadar from './components/RiskRadar';
import GlossaryTooltip from './components/GlossaryTooltip';
import PitchOutline from './components/PitchOutline';
import InvestorMatches from './components/InvestorMatches';
import OutreachDraft from './components/OutreachDraft';
import ScalingAdvisor from './components/ScalingAdvisor';
import ReportCard from './components/ReportCard';
import { motion, AnimatePresence } from 'framer-motion';
import { useValidation } from './hooks/useValidation';

function App() {
  const [idea, setIdea] = useState('');
  const [revealComplete, setRevealComplete] = useState(false);
  const [activeTab, setActiveTab] = useState('report');
  const [selectedInvestor, setSelectedInvestor] = useState(null);
  const { isAnalyzing, results, rawReport, error, validateIdea, reset, setIsAnalyzing } = useValidation();

  const handleAnalyze = () => {
    if (!idea.trim()) return;
    setRevealComplete(false);
    setActiveTab('report');
    setSelectedInvestor(null);
    validateIdea(idea);
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
                  {error && (
                    <div className="text-red-500 text-sm font-sans px-2">
                      {error}
                    </div>
                  )}
                  <div className="flex justify-end mt-2">
                    <button 
                      onClick={handleAnalyze}
                      disabled={isAnalyzing}
                      className="w-full md:w-auto bg-sage text-white px-8 py-3 min-h-[44px] rounded-[var(--radius)] font-medium text-lg hover:shadow-md hover:bg-opacity-95 transition-all duration-300 active:scale-[0.98] disabled:opacity-50"
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
                  <div className="flex gap-6 border-b border-gray-200 w-full overflow-x-auto pb-2">
                    {['report', 'pitch', 'investors', 'scaling'].map(tab => (
                      <button
                        key={tab}
                        onClick={() => setActiveTab(tab)}
                        className={`text-lg font-serif pb-2 border-b-2 transition-colors whitespace-nowrap ${
                          activeTab === tab 
                            ? 'border-sage text-sage' 
                            : 'border-transparent text-charcoal hover:text-sage'
                        }`}
                      >
                        {tab === 'report' ? 'Validation Report' :
                         tab === 'pitch' ? 'Pitch Outline' :
                         tab === 'investors' ? 'Investors & Outreach' :
                         'Scaling Advisor'}
                      </button>
                    ))}
                    <div className="flex-grow"></div>
                    <button 
                      onClick={() => {
                        reset();
                        setRevealComplete(false);
                        setIdea('');
                        setSelectedInvestor(null);
                      }}
                      className="text-sage hover:text-sage-light transition-colors font-medium whitespace-nowrap ml-4"
                    >
                      Start Over
                    </button>
                  </div>
                </div>

                {activeTab === 'report' && (
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-8">
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
                        {results.marketReasoning || "The market context indicates promising areas, but clear positioning will be required to capture a substantial share."}
                      </p>
                    </div>

                    <ReportCard score={results.score} summary={results.scoreSummary} />
                  </motion.div>
                )}

                {activeTab === 'pitch' && (
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                    <PitchOutline report={rawReport} />
                  </motion.div>
                )}

                {activeTab === 'investors' && (
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-8">
                    <InvestorMatches 
                      report={rawReport} 
                      onSelectInvestor={setSelectedInvestor} 
                      selectedInvestor={selectedInvestor}
                    />
                    {selectedInvestor && (
                      <OutreachDraft report={rawReport} investor={selectedInvestor} />
                    )}
                  </motion.div>
                )}

                {activeTab === 'scaling' && (
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                    <ScalingAdvisor ideaText={idea} />
                  </motion.div>
                )}

              </motion.div>
            )}
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
}

export default App;
