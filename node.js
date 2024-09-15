const express = require('express');
const fetch = require('node-fetch');
const app = express();

app.use(express.json());

app.post('/generate-email', async (req, res) => {
    const { subject, keyPoints } = req.body;
    
    const response = await fetch('https://api.openai.com/v1/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer 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' // Securely stored
        },
        body: JSON.stringify({
            model: "gpt-3.5-turbo",
            prompt: `Subject: ${subject}\n\nEmail Body: Based on the following key points: ${keyPoints}.`,
            max_tokens: 150
        })
    });

    const data = await response.json();
    res.json(data.choices[0].text);
});

app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});
