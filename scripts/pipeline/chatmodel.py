import streamlit as st
from openai import AzureOpenAI

# ✅ Initialize Azure OpenAI Client
client = AzureOpenAI(
    api_key=st.secrets["Gptkey"],  # ✅ Use your Azure OpenAI GPT-4o key
    api_version="2024-10-21",   # ✅ Ensure this is the correct API version
    azure_endpoint=st.secrets["Gptendpoint"]  # ✅ Use your Azure OpenAI GPT-4o endpoint
)

def chat_with_gpt4o(prompt):
    """
    Sends the user prompt to GPT-4o with streaming enabled for faster responses.
    """
    if not prompt:
        return "No input provided."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            stream=True  # ✅ Enable streaming
        )

        full_response = ""
        for chunk in response:
            if chunk.choices:
                full_response += chunk.choices[0].delta.content or ""

        return full_response.strip()

    except Exception as e:
        return f"Error: {str(e)}"