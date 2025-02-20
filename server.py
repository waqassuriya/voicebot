import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google.generativeai import GenerativeModel, configure
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Google Generative AI
API_KEY = os.getenv("API_KEY")  
if not API_KEY:
    raise ValueError("API_KEY is missing in the .env file")

configure(api_key=API_KEY)

# Load the Gemini model
model = GenerativeModel(model_name="gemini-2.0-flash")

# Request body model
class ChatRequest(BaseModel):
    message: str

@app.post("/api/assistant")
async def chat_with_assistant(request: ChatRequest):
    try:
        response = model.generate_content(request.message)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to communicate with Gemini API: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 5000))  # Default to 8000 if not set in .env
    uvicorn.run(app, host="0.0.0.0", port=port)
