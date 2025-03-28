from google.cloud import dialogflow_v2 as dialogflow
import os

# Manually set credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "E:\\chatbot-backend\\dialogflow-key.json"

DIALOGFLOW_PROJECT_ID = "bottest-9qb9"
session_id = "test_session"

def detect_intent_texts(session_id, text):
    """Send user message to Dialogflow and get a response."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)
    
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text  # Get chatbot's reply

print(detect_intent_texts(session_id, "Hello"))
