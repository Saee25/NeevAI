import React, { useState } from 'react'
import Card from './components/Card'

function App() {
  const [idea, setIdea] = useState('');

  return (
    <div className="min-h-screen p-6 md:p-12 flex flex-col items-center">
      <div className="w-full max-w-3xl space-y-12 md:space-y-16 mt-4 md:mt-8">
        <header className="text-center space-y-4">
          <h1 className="text-4xl md:text-5xl font-medium text-sage tracking-tight">AI Co-Founder</h1>
          <p className="text-charcoal-muted text-lg md:text-xl font-light tracking-wide">
            Startup Idea Validation Platform
          </p>
        </header>

        <main>
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
                  className="w-full md:w-auto bg-sage text-white px-8 py-3 min-h-[44px] rounded-[var(--radius)] font-medium text-lg hover:shadow-md hover:bg-opacity-95 transition-all duration-300 active:scale-[0.98]"
                >
                  Analyze Idea
                </button>
              </div>
            </div>
          </Card>
        </main>
      </div>
    </div>
  )
}

export default App
