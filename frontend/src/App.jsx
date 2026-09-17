import React, { useState } from 'react';
import Card from './components/Card';
import AgentReveal from './components/AgentReveal';
import ReadinessScore from './components/ReadinessScore';
import MarketChart from './components/MarketChart';
import CompetitorList from './components/CompetitorList';
import RiskRadar from './components/RiskRadar';
import PitchOutline from './components/PitchOutline';
import InvestorMatches from './components/InvestorMatches';
import OutreachDraft from './components/OutreachDraft';
import ScalingAdvisor from './components/ScalingAdvisor';
import ReportCard from './components/ReportCard';
import { motion, AnimatePresence } from 'framer-motion';
import { useValidation } from './hooks/useValidation';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

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

          {(isAnalyzing || (results && !revealComplete)) && (
            <AgentReveal 
              results={results} 
              isAnalyzing={isAnalyzing}
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
                      <ReadinessScore 
                        score={results.score} 
                        summary={
                          results.score >= 70
                            ? "High readiness: strong market opportunity and addressable risks identified."
                            : results.score >= 40
                            ? "Moderate readiness: promising idea with key execution and competitive hurdles to navigate."
                            : "Early-stage: substantial market and regulatory risks require deeper proof-of-concept."
                        } 
                      />
                      <RiskRadar data={results.riskData} />
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                      <MarketChart data={results.marketData} />
                      <CompetitorList competitors={results.competitors} />
                    </div>

                    {results.unverifiedClaims && results.unverifiedClaims.length > 0 && (
                      <div className="bg-amber-50 border border-amber-200 p-6 rounded-[var(--radius)]">
                        <div className="flex items-center gap-2 mb-3">
                          <span className="text-amber-600 text-lg">⚠️</span>
                          <h3 className="text-lg font-serif text-amber-900">Grounding Notice: Unverified Claims</h3>
                        </div>
                        <p className="text-xs text-amber-800 mb-3">
                          The following claim(s) from the synthesized report did not match direct evidence in the retrieved case studies and require independent founder verification:
                        </p>
                        <ul className="list-disc list-inside text-xs text-amber-900 space-y-1">
                          {results.unverifiedClaims.map((claim, idx) => (
                            <li key={idx} className="font-sans leading-relaxed">{claim}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    <div className="bg-white p-8 rounded-[var(--radius)] shadow-sm space-y-4">
                      <div className="flex justify-between items-center border-b border-gray-100 pb-3">
                        <h3 className="text-2xl font-serif text-charcoal">Executive Summary & Validation Report</h3>
                        <span className="text-xs font-sans uppercase tracking-wider text-sage bg-sage/10 px-3 py-1 rounded-full font-medium">
                          Multi-Agent Grounded
                        </span>
                      </div>
                      <div className="prose prose-sm md:prose-base prose-sage max-w-none text-charcoal-muted leading-relaxed font-sans pt-2">
                        <ReactMarkdown 
                          remarkPlugins={[remarkGfm]}
                          components={{
                            h1: ({node, ...props}) => <h1 className="text-2xl font-serif text-charcoal mt-6 mb-4" {...props} />,
                            h2: ({node, ...props}) => <h2 className="text-xl font-serif text-charcoal mt-5 mb-3 border-b pb-2" {...props} />,
                            h3: ({node, ...props}) => <h3 className="text-lg font-medium text-charcoal mt-4 mb-2" {...props} />,
                            p: ({node, ...props}) => <p className="mb-4" {...props} />,
                            ul: ({node, ...props}) => <ul className="list-disc list-outside ml-5 mb-4 space-y-1" {...props} />,
                            ol: ({node, ...props}) => <ol className="list-decimal list-outside ml-5 mb-4 space-y-1" {...props} />,
                            li: ({node, ...props}) => <li className="pl-1" {...props} />,
                            table: ({node, ...props}) => (
                              <div className="overflow-x-auto mb-6 border border-gray-200 rounded-lg shadow-sm">
                                <table className="w-full text-left border-collapse" {...props} />
                              </div>
                            ),
                            thead: ({node, ...props}) => <thead className="bg-sage/10 text-sage border-b border-gray-200" {...props} />,
                            th: ({node, ...props}) => <th className="p-3 font-semibold text-sm" {...props} />,
                            td: ({node, ...props}) => <td className="p-3 border-b border-gray-100 last:border-b-0 text-sm align-top" {...props} />,
                            strong: ({node, ...props}) => <strong className="font-semibold text-charcoal" {...props} />,
                          }}
                        >
                          {results.scoreSummary}
                        </ReactMarkdown>
                      </div>
                    </div>

                    <ReportCard 
                      score={results.score} 
                      summary={results.scoreSummary} 
                      marketData={results.marketData}
                      risks={results.rawRisks}
                    />
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
