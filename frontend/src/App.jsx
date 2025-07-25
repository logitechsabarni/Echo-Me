import React, { useState, useEffect } from 'react';
import axios from 'axios';

// ✅ Use your live backend URL here
const BASE_URL = import.meta.env.VITE_API_URL;

function App() {
  const [form, setForm] = useState({ to: '', from: '', content: '', unlock_date: '' });
  const [messages, setMessages] = useState([]);

  const fetchMessages = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/view`);
      setMessages(res.data);
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  useEffect(() => {
    fetchMessages();
  }, []);

  const sendMessage = async () => {
    try {
      await axios.post(`${BASE_URL}/send`, form);
      alert('Message scheduled!');
      setForm({ to: '', from: '', content: '', unlock_date: '' });
      fetchMessages();
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1>EchoMe</h1>
      <div style={{ marginBottom: '1rem' }}>
        <input placeholder="To" value={form.to} onChange={e => setForm({ ...form, to: e.target.value })} /><br />
        <input placeholder="From" value={form.from} onChange={e => setForm({ ...form, from: e.target.value })} /><br />
        <textarea placeholder="Message" value={form.content} onChange={e => setForm({ ...form, content: e.target.value })}></textarea><br />
        <input type="date" value={form.unlock_date} onChange={e => setForm({ ...form, unlock_date: e.target.value })} /><br />
        <button onClick={sendMessage}>Schedule Message</button>
      </div>

      <h2>Unlocked Messages</h2>
      <ul>
        {messages.map((msg, index) => (
          <li key={index}>
            <strong>From:</strong> {msg.from} <strong>To:</strong> {msg.to}<br />
            <strong>Message:</strong> {msg.content}<br />
            <strong>Unlock Date:</strong> {msg.unlock_date}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
