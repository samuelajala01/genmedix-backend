from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import os

import google.generativeai as genai


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)


if GOOGLE_API_KEY:
  print("API key is present")

########### GEMINI STUFF ################

# Set up the model
generation_config = {
  "temperature": 0.3,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model=genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction="You are a mental health/therapy assistant. Your name is Eliza. you are created by GenMedix")

# to enable multi-turn conversations(chat)
# use chat.history to access chat history
chat = model.start_chat(history=[])



#best way to chat with the model
# response = chat.send_message("who are you")










########## API STUFF #############

app = FastAPI()

origins = [
    "https://genmedix.vercel.app",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str

# Run the application using: uvicorn main:app --reload

# Define the POST endpoint
@app.post("/chat")
async def ask_question(question: Question):
    try:
        # Extract the question from the request body
        user_question = question.question
        
        # chat = model.start_chat(history=[])
        # Generate a response using the chat model
        model_response = chat.send_message(user_question)
        print(chat.history)
        
        # Return the model's response
        return {"response": model_response.text}
    except Exception as e:
        # Handle exceptions and return an HTTP 500 error with the exception message
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat_history")
async def get_chats():
    try:
        history = chat.history
        print(history)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

if __name__ == "__main__":
    uvicorn.run("main", host="0.0.0.0", port=8000, log_level="info")

# Run the application with: uvicorn main:app --reload on the terminal    