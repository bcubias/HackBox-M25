import streamlit as st
from openai import AzureOpenAI

# Use the new GPT-4o key and endpoint from secrets.toml
client = AzureOpenAI(
    api_key=st.secrets["Gptkey"],  # ✅ Use your new Azure OpenAI GPT-4o key
    api_version="2024-10-21",   # ✅ Ensure this is the latest API version
    azure_endpoint=st.secrets["Gptendpoint"]  # ✅ Use your new Azure OpenAI GPT-4o endpoint
)

def grammar_check(text):
    """
    Uses Azure OpenAI GPT-4o to check and correct grammar mistakes.
    
    :param text: The user-provided input.
    :return: A tuple containing corrected text and a log message.
    """
    if not text:
        return text, "No text provided."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # ✅ Ensure this matches your Azure OpenAI deployment name
            messages=[
                {"role": "system", "content": "You are a grammar correction assistant. Correct any grammar and spelling mistakes."},
                {"role": "user", "content": text}
            ]
        )

        corrected_text = response.choices[0].message.content.strip()
        if corrected_text.lower() != text.lower():
            return corrected_text, "Grammar corrected using GPT-4o."
        else:
            return text, "No grammar mistakes found."

    except Exception as e:
        return text, f"Grammar check failed: {str(e)}"