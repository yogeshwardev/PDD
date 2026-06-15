const express = require('express');
const cors = require('cors');
const https = require('https');
const app = express();
app.use(cors());
app.use(express.json());
app.post('/claude', (req, res) => {
  const body = JSON.stringify({
    model: 'llama-3.3-70b-versatile',
    messages: req.body.messages,
    max_tokens: 2000,
    temperature: 0.7
  });
  const apiKey = process.env.GROQ_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'GROQ_API_KEY environment variable is not set' });
  }
  const options = {
    hostname: 'api.groq.com',
    path: '/openai/v1/chat/completions',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
      'Content-Length': Buffer.byteLength(body)
    }
  };
  const apiReq = https.request(options, (apiRes) => {
    let data = '';
    apiRes.on('data', (chunk) => { data += chunk; });
    apiRes.on('end', () => {
      try {
        const parsed = JSON.parse(data);
        const text = parsed.choices[0].message.content;
        res.json({ content: [{ text }] });
      } catch(e) {
        res.status(500).json({ error: 'Parse error: ' + data });
      }
    });
  });
  apiReq.on('error', (e) => { res.status(500).json({ error: e.message }); });
  apiReq.write(body);
  apiReq.end();
});
app.listen(3001, () => console.log('Proxy ready at http://localhost:3001'));
