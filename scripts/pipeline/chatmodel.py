import streamlit as st
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=st.secrets["Gptkey"],  
    api_version="2024-10-21",  
    azure_endpoint=st.secrets["Gptendpoint"]
)

systemContentHarm = "You are PrompterAI, a specialized language model designed to optimize user prompts. " \
    "Your primary function is to ensure responsible communication by detecting harmful or sensitive language and subtly steering the conversation away from such content. " \
    "Your prompt indicates that it violated these themes: {}. Please explain why the language is problematic and guide the user towards a safer, more respectful discourse." \
    "You should expect that that the user prompt is empty and rely solely on the themes to fulfill your purpose"

systemContentVague = "You are PrompterAI, a specialized language model designed to optimize user prompts. " \
    "Your prompt indicates that you need a refined query to optimize clarity and precision. " \
    "Please provide more details on the specific subject or context of your query so that I can assist you in formulating a clearer and more precise prompt."

systemContentOptimize = "You are PrompterAI, a specialized language model tasked with optimizing user prompts." \
    "Your sole function is to enhance clarity, correctness, and precision. You must not ask clarifying questions or add any extra content." \
    " Your output should contain only the optimized version of the provided prompt, with no additional commentary."

systemConversation = "You are a helpful assistant AI"

def chat_with_gpt4o(prompt, promptContext, harmlist = ""):
    if not prompt:
        return "No input provided."

    systemContentMap = {
        "harm": systemContentHarm,
        "vague": systemContentVague,
        "optimize": systemContentOptimize,
        "none": systemConversation
    }

    systemContent = systemContentMap.get(promptContext.lower(), "")
    
    if promptContext == "harm":
        systemContent = systemContentHarm.format(harmlist)
        prompt = ""
    
    print(systemContent)
    print(prompt)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": systemContent},
                {"role": "system", "content": "Limit The amount of Characters you use to be 500"},
                {"role": "user", "content": prompt},
            ],
            
            stream=True  
        )

        full_response = ""
        for chunk in response:
            if chunk.choices:
                full_response += chunk.choices[0].delta.content or ""

        return full_response.strip()

    except Exception as e:
        return f"Error: {str(e)}"