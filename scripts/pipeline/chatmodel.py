import streamlit as st
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=st.secrets["Gptkey"],  
    api_version="2024-10-21",  
    azure_endpoint=st.secrets["Gptendpoint"]  
)

def chat_with_gpt4o(prompt):
    if not prompt:
        return "No input provided."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            stream=True  
        )

        full_response = ""
        for chunk in response:
            if chunk.choices:
                full_response += chunk.choices[0].delta.content or ""

        return full_response.strip()

    except Exception as e:
        return f"Error: {str(e)}"