require('dotenv').config();
const express = require("express");
const cors = require("cors");
const { GoogleGenerativeAI } = require("@google/generative-ai");


const app = express();
app.use(cors());
app.use(express.json());

const API_KEY = process.env.API_KEY// Replace with your actual API key
const genAI = new GoogleGenerativeAI(API_KEY);

const model = genAI.getGenerativeModel({
  model: "gemini-2.0-flash",
});

app.post("/api/assistant", async (req, res) => {
  const { message } = req.body;
  if (!message) {
    return res.status(400).json({ error: "Message is required" });
  }

  try {
    const chatSession = model.startChat({
      history: [
        {
          role: "user",
          parts: [{ text: message }],
        },
      ],
    });

    const result = await chatSession.sendMessage(message);
    res.json({ response: result.response.text() });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Failed to communicate with Gemini API" });
  }
});

// Use Render's PORT environment variable, defaulting to 5000 locally
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
