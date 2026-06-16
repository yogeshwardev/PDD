const express = require('express');
const cors = require('cors');
const https = require('https');
const app = express();

// Security: restrict CORS to known origins only
const ALLOWED_ORIGINS = [
  'http://localhost:8081',
  'http://localhost:19006',
  'https://dinesh-2005d.github.io',
];
app.use(cors({
  origin: function (origin, callback) {
    // Allow requests with no origin (mobile apps, curl)
    if (!origin || ALLOWED_ORIGINS.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  methods: ['POST'],
  allowedHeaders: ['Content-Type'],
}));

// Security: add basic security headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Referrer-Policy', 'no-referrer');
  next();
});

app.use(express.json({ limit: '10kb' })); // Security: limit request body size

// Security: input validation helper
function validateMessages(messages) {
  if (!Array.isArray(messages)) return false;
  if (messages.length === 0 || messages.length > 50) return false;
  for (const msg of messages) {
    if (typeof msg !== 'object' || !msg) return false;
    if (!['user', 'assistant', 'system'].includes(msg.role)) return false;
    if (typeof msg.content !== 'string') return false;
    if (msg.content.length > 8000) return false;
  }
  return true;
}

app.post('/claude', (req, res) => {
  const { messages } = req.body || {};

  // Security: validate input before forwarding to external API
  if (!validateMessages(messages)) {
    return res.status(400).json({ error: 'Invalid request: messages must be a non-empty array with valid roles and string content' });
  }

  const apiKey = process.env.GROQ_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'Server configuration error' });
  }

  const body = JSON.stringify({
    model: 'llama-3.3-70b-versatile',
    messages: messages,
    max_tokens: 2000,
    temperature: 0.7
  });

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
        if (!parsed.choices || !parsed.choices[0] || !parsed.choices[0].message) {
          return res.status(502).json({ error: 'Unexpected response from AI service' });
        }
        const text = parsed.choices[0].message.content;
        res.json({ content: [{ text }] });
      } catch (e) {
        // Security: do not echo raw upstream response to client
        res.status(502).json({ error: 'Failed to parse AI service response' });
      }
    });
  });

  apiReq.on('error', () => {
    // Security: do not expose internal error details
    res.status(503).json({ error: 'AI service unavailable' });
  });

  // Security: enforce request timeout
  apiReq.setTimeout(30000, () => {
    apiReq.destroy();
    res.status(504).json({ error: 'Request timed out' });
  });

  apiReq.write(body);
  apiReq.end();
});

// Security: reject unknown routes
app.use((req, res) => {
  res.status(404).json({ error: 'Not found' });
});

app.listen(3001, '127.0.0.1', () => console.log('Proxy ready at http://localhost:3001'));
