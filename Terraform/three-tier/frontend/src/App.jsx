import React, { useState, useEffect } from 'react';
import './App.css';

// const api = "https://scaling-space-halibut-qv4w4xjq5xjh6gx-5000.app.github.dev/feedback"
const api = "http://localhost:5000/feedback"

function App() {
  const [name, setName] = useState('');
  const [comment, setComment] = useState('');
  const [feedbacks, setFeedbacks] = useState([]);

  useEffect(() => {
    // Fetch feedback from the backend
    fetch(api)
      .then(response => response.json())
      .then(data => setFeedbacks(data));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();

    const newFeedback = { name, comment };

    // Send feedback to the backend
    fetch(api, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newFeedback),
    })
    .then(response => response.json())
    .then(data => {
      // Update the feedback list with the new feedback
      setFeedbacks([...feedbacks, newFeedback]);
      setName('');
      setComment('');
    })
    .catch(error => console.error('Error:', error));
  };

  return (
    <div className="App">
      <h1>Feedback Form</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <input 
            type="text" 
            placeholder="Your Name" 
            value={name} 
            onChange={(e) => setName(e.target.value)} 
            required 
          />
        </div>
        <div>
          <textarea 
            placeholder="Your Feedback" 
            value={comment} 
            onChange={(e) => setComment(e.target.value)} 
            required 
          />
        </div>
        <button type="submit">Submit</button>
      </form>

      <h2>Feedback List</h2>
      <ul>
        {feedbacks.map(feedback => (
          <li key={feedback.id}>
            <strong>{feedback.name}:</strong> {feedback.comment}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
