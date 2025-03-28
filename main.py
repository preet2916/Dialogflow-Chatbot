from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from google.cloud import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env
load_dotenv()

# Manually set credentials for Google Dialogflow
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "E:\\chatbot-backend\\dialogflow-key.json"

# Read credentials from .env
creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_json

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "FastAPI is running!"}

# ✅ Define request model
class ChatRequest(BaseModel):
    session_id: str
    message: str

# ✅ Dialogflow Project Details
DIALOGFLOW_PROJECT_ID = "bottest-9qb9"

def detect_intent_texts(session_id, text):
    """Send user message to Dialogflow and get a response."""
    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)

        text_input = dialogflow.TextInput(text=text, language_code="en")
        query_input = dialogflow.QueryInput(text=text_input)
        
        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
        return response.query_result.fulfillment_text  # Get chatbot's reply

    except Exception as e:
        print(f"Error: {e}")  # Logs the error
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ✅ API Endpoint to chat with Dialogflow
@app.post("/chat")
def chat(request: ChatRequest):
    reply = detect_intent_texts(request.session_id, request.message)
    return {"reply": reply}
