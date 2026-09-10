import React, { useEffect, useState } from 'react'

function App() {
  const [helloMessage, setHelloMessage] = useState('Loading backend status...');

  useEffect(() => {
    // Attempt to fetch from backend
    fetch('http://127.0.0.1:8000/api/hello')
      .then(res => res.json())
      .then(data => setHelloMessage(data.message))
      .catch(err => setHelloMessage('Backend not reachable: ' + err.message));
  }, []);

  return (
    <div className="min-h-screen p-8 max-w-4xl mx-auto">
      <header className="mb-12">
        <h1 className="text-4xl font-bold text-primary mb-2">AI Co-Founder</h1>
        <p className="text-secondary text-lg">Startup Idea Validation Platform</p>
      </header>

      <main>
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <h2 className="text-2xl mb-4">Backend Connection Status</h2>
          <div className="p-4 bg-gray-50 rounded-lg text-sm font-mono">
            {helloMessage}
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
