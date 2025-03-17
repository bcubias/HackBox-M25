import requests
import streamlit as st

def chat_with_gpt4o(prompt):
    """
    Sends the user prompt to GPT-4o via Azure OpenAI and retrieves the AI's response.
    """
    api_key = st.secrets["Gptkey"] 
    endpoint = st.secrets["Gptendpoint"] 

    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    
    deployment_name = "gpt-4o"  

    data = {
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(
            f"{endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version=2024-10-21",
            headers=headers, json=data
        )

        response_json = response.json()
        print("GPT-4o Full Response:", response_json)  

        if "choices" in response_json:
            return response_json["choices"][0]["message"]["content"]
        else:
            return f"Error: 'choices' key not found in response - {response_json}"

    except Exception as e:
        return f"Error: {str(e)}"