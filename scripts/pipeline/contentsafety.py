import streamlit as st
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

key = st.secrets.Azurekey
endpoint = st.secrets.Azureendpoint

def safety_check(message):
    # Create a Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Construct a request
    request = AnalyzeTextOptions(text=message)

    # Analyze text
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    harm = [] 

    hate_result = next(item for item in response.categories_analysis if item.category == TextCategory.HATE)
    harm.append("hate") if hate_result.severity >= 4 else ""
    self_harm_result = next(item for item in response.categories_analysis if item.category == TextCategory.SELF_HARM)
    harm.append("self") if self_harm_result.severity >= 4 else ""
    sexual_result = next(item for item in response.categories_analysis if item.category == TextCategory.SEXUAL)
    harm.append("sexual") if sexual_result.severity >= 4 else ""
    violence_result = next(item for item in response.categories_analysis if item.category == TextCategory.VIOLENCE)
    harm.append("violence") if violence_result.severity >= 4 else ""

    return max(hate_result.severity, self_harm_result.severity, sexual_result.severity, violence_result.severity), harm