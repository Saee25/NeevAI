const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function fetchWithHandling(url, options = {}) {
  const timeoutMs = options.timeout || 600000;
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(`${API_BASE}${url}`, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });
    clearTimeout(id);

    if (!response.ok) {
      if (response.status === 429) {
        throw new Error("You're going a bit too fast! Please try again in a minute.");
      }
      const data = await response.json().catch(() => ({}));
      throw new Error(data.detail || "Something didn't load right — try again in a moment.");
    }

    return await response.json();
  } catch (error) {
    console.error("[API Error] fetchWithHandling failed:", error);
    clearTimeout(id);
    if (error.name === 'AbortError') {
      throw new Error("Request timed out. The server took too long to respond.");
    }
    if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
      throw new Error("Could not connect to the server. Please check your connection.");
    }
    throw error;
  }
}

export const api = {
  validateIdea: (idea_text) => 
    fetchWithHandling('/validate/', {
      method: 'POST',
      body: JSON.stringify({ idea_text })
    }),
    
  getScalingAdvice: (idea_text, revenue_context) =>
    fetchWithHandling('/validate/scaling-advice', {
      method: 'POST',
      body: JSON.stringify({ idea_text, revenue_context: revenue_context || "" })
    }),

  generatePitchOutline: (report) =>
    fetchWithHandling('/generate/pitch-outline', {
      method: 'POST',
      body: JSON.stringify({ report })
    }),

  generateInvestorMatches: (report) =>
    fetchWithHandling('/generate/investor-matches', {
      method: 'POST',
      body: JSON.stringify({ report })
    }),

  generateOutreachDraft: (report, investor) =>
    fetchWithHandling('/generate/outreach-draft', {
      method: 'POST',
      body: JSON.stringify({ report, investor })
    })
};
