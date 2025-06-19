import React, { useState } from 'react';

export default function App() {
  const [quotes, setQuotes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchQuotes = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/quotes');
      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }
      const data = await res.json();
      setQuotes(data);
    } catch (err) {
      setError(`Error fetching quotes: ${err.message}`);
      console.error('Error fetching quotes:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Quotes Database</h1>
      <p>Click the button below to load quotes from the database via the Flask API.</p>
      
      <button 
        onClick={fetchQuotes}
        style={{
          padding: '10px 15px',
          backgroundColor: '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '16px',
          marginBottom: '20px'
        }}
        disabled={loading}
      >
        {loading ? 'Loading...' : 'Load Quotes'}
      </button>
      
      {error && (
        <div style={{ color: 'red', marginBottom: '20px' }}>
          {error}
        </div>
      )}
      
      {quotes.length > 0 ? (
        <ul style={{ listStyleType: 'none', padding: 0 }}>
          {quotes.map(q => (
            <li key={q.id} style={{ 
              padding: '15px', 
              marginBottom: '10px', 
              borderLeft: '4px solid #4CAF50',
              backgroundColor: '#f9f9f9'
            }}>
              "{q.quote}" - <strong>{q.author}</strong>
            </li>
          ))}
        </ul>
      ) : !loading && !error && (
        <p>No quotes loaded yet. Click the button above to fetch quotes.</p>
      )}
    </div>
  );
}