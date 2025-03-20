import streamlit as st
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=st.secrets["Gptkey"],  
    api_version="2024-10-21",  
    azure_endpoint=st.secrets["Gptendpoint"]  
)

systemContentHarm = "You are an Michael Jackson and the user entered a harmful message. \n"\
          " Your role is to move him away from this topic in order to prevent him from saying another harmful message"

systemContentVague = "You are a British Santa clause and you require greater context for the prompt"

systemContentOptimize = "You are PrompterAI, a specialized language model designed to optimize user prompts. " \
    "Your primary function is to enhance clarity, correctness, and precision by identifying and resolving grammatical errors, " \
    "incomplete queries, and ambiguous inputs. PrompterAI also ensures responsible communication by detecting harmful or sensitive language, " \
    "offering safe and ethical alternatives. Your response should be the optimized version of the input prompt only, with no additional explanation or commentary."

systemConversation = "You are an helpful assistant AI"

def chat_with_gpt4o(prompt, promptContext = ""):
    if not prompt:
        return "No input provided."

    systemContentMap = {
        "harm": systemContentHarm,
        "vague": systemContentVague,
        "optimize": systemContentOptimize,
        "none": systemConversation
    }

    systemContent = systemContentMap.get(promptContext.lower(), "")
    
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
    