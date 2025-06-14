import React, { useState, useEffect } from 'react';

function App() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [response, setResponse] = useState(null);
  const [posts, setPosts] = useState([]);

  // Fetch posts on component mount
  useEffect(() => {
    fetch('http://localhost:8000/posts/')
      .then(res => res.json())
      .then(data => setPosts(data))
      .catch(console.error);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/posts/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content }),
      });
      const data = await res.json();
      setResponse(data);
      // Refresh posts list after submit
      setPosts(prev => [data, ...prev]);
      setTitle('');
      setContent('');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: 'auto', padding: 20 }}>
      <h1>Create a Post</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title:</label>
          <input
            value={title}
            onChange={e => setTitle(e.target.value)}
            required
            style={{ width: '100%', padding: '8px' }}
          />
        </div>
        <div style={{ marginTop: 10 }}>
          <label>Content:</label>
          <textarea
            value={content}
            onChange={e => setContent(e.target.value)}
            required
            style={{ width: '100%', padding: '8px' }}
          />
        </div>
        <button type="submit" style={{ marginTop: 10 }}>Submit</button>
      </form>

      {response && (
        <div style={{ marginTop: 20 }}>
          <h3>Response from backend:</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}

      <h2 style={{ marginTop: 40 }}>Posts List</h2>
      <ul>
        {posts.map(post => (
          <li key={post.slug}>
            <strong>{post.title}</strong> — {post.created_at}
            <div dangerouslySetInnerHTML={{ __html: post.html }} />
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
