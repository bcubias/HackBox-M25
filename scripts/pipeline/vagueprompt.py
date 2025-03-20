import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Load Azure credentials from Streamlit secrets
key = st.secrets["Azurekey"]
endpoint = st.secrets["Azureendpoint"]

# Initialize Azure Text Analytics Client
def authenticate_client():
    return TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

text_analytics_client = authenticate_client()

def analyze_prompt(message):
    # Extract named entities
    try:
        entity_response = text_analytics_client.recognize_entities([message])
        entities = {entity.text: entity.category for doc in entity_response for entity in doc.entities}
    except Exception as e:
        print(f"NER analysis failed for input: {message}\nError: {e}")
        entities = {}

    if not entities:
        return {
            "status": "vague",
            "message": "⚠️ This prompt lacks a specific noun or proper entity. Please include a name, place, or event."
        }

    return {
        "status": "clear",
        "entities_detected": entities
    }