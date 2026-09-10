import { useState } from 'react';
import { api } from '../lib/api';

const extractNumber = (str) => {
  if (!str) return 0;
  const match = str.match(/[\d.]+/);
  if (!match) return 0;
  let num = parseFloat(match[0]);
  if (str.toLowerCase().includes('b') || str.toLowerCase().includes('billion')) num *= 1000;
  // Let's assume M is the base unit for numbers in the chart for visual purposes,
  // or B. If it's relative, it doesn't matter too much as long as it parses something.
  return num;
};

export const useValidation = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [rawReport, setRawReport] = useState(null);

  const validateIdea = async (idea_text) => {
    if (idea_text.length < 50) {
      setError("Please share a bit more detail about your idea (at least 50 characters).");
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setResults(null);
    setRawReport(null);

    try {
      const data = await api.validateIdea(idea_text);
      setRawReport(data);
      
      const tamNum = extractNumber(data.market_findings?.tam_estimate);
      const samNum = extractNumber(data.market_findings?.sam_estimate);
      const somNum = extractNumber(data.market_findings?.som_estimate);

      const mappedResults = {
        score: data.readiness_score || 0,
        scoreSummary: data.summary || "No summary provided.",
        marketData: [
          { name: 'TAM', value: tamNum || 100, text: data.market_findings?.tam_estimate || '' },
          { name: 'SAM', value: samNum || 35, text: data.market_findings?.sam_estimate || '' },
          { name: 'SOM', value: somNum || 10, text: data.market_findings?.som_estimate || '' }
        ],
        rawMarket: data.market_findings,
        rawRisks: data.risk_findings,
        marketReasoning: data.market_findings?.reasoning || "",
        competitors: (data.competitor_findings?.similar_startups || []).map(c => ({
          name: c.name,
          outcome: c.outcome,
          summary: c.summary,
          sourceLink: c.source_url
        })),
        positioningNotes: data.competitor_findings?.positioning_notes || "",
        riskData: [
          { subject: 'Market', value: (data.risk_findings?.market_risk || 1) * 20 },
          { subject: 'Execution', value: (data.risk_findings?.execution_risk || 1) * 20 },
          { subject: 'Funding', value: (data.risk_findings?.funding_risk || 1) * 20 },
          { subject: 'Regulatory', value: (data.risk_findings?.regulatory_risk || 1) * 20 }
        ],
        riskNotes: data.risk_findings?.notes || [],
        unverifiedClaims: data.unverified_claims || []
      };
      
      setResults(mappedResults);
    } catch (err) {
      setError(err.message || "Something didn't load right — try again in a moment.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const reset = () => {
    setResults(null);
    setRawReport(null);
    setError(null);
    setIsAnalyzing(false);
  };

  return {
    isAnalyzing,
    results,
    rawReport,
    error,
    validateIdea,
    reset,
    setIsAnalyzing
  };
};
