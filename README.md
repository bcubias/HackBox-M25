# HackBox-M25
Microsoft HackBox Repo for March 2025

![Illustration2](https://github.com/user-attachments/assets/1c883944-2276-4496-88b8-9e4b9cf0b25c)

# PrompterAI
PrompterAI is a preprocessing layer that improves AI and LLM response quality by optimizing user prompts for clarity and completeness and flagging any potentially unethical or harmful messages.

The current version of PrompterAI in this GitHub repository showcases a website where users can create chats and submit prompts to ChatGPT. After the user submits a prompt either through text or voice, the initial message will be scanned for harmful, explicit, and vague messaging, then keywords will be extracted and the prompt will be run through an AI along with keywords to create a final optimized prompt. The new prompt is sent to ChatGPT, producing a more accurate and relevant response.

This middle layer in between user and AI ensures safety and removes any bias, danger, and potential risk from reaching the AI.

# Features and Technology Used
- Website: Uses Streamlit to build the webapp
- Speech to Text: Azure Cognitive Services detects speech and translates it into text
- Text Analysis: Uses Azure AI language and Azure AI Content Safety to analyze user prompt for harmful speech and keywords
- Prompt Optimizer: Azure OpenAI is used to to convert the user prompt into an optimized prompt
- Chatbot Model: Uses ChatGPT-4o 

# Demo Video
https://youtu.be/7sTEs-xEod4

# System Architecture
## System Design
![Untitled](https://github.com/user-attachments/assets/73f9dbf5-09d6-4eb7-8762-aba1f4153274)

## Process Flow
![Untitled](https://github.com/user-attachments/assets/80381a8b-eb9c-4f37-a2f6-a5570649d4dd)

# Running Locally
Prerequisites
- Python version
- Python packages
- Azure Resource keys

Clone Project
```
git clone 
```
Install Dependencies
```
pip install -r requirements.txt
```
Create .streamlit folder
```
mkdir .streamlit
```
Create a secrets.toml file in the .streamlit fodler
Secrets Variables (Your Azure Resources keys)
```
Azurekey = ""
Azureendpoint = ""
speech_region = ""

Gptendpoint = ""
Gptkey = ""
```
Run streamlit server
```
.\run.bat
```
# Future Improvements
- Companies can use the middle layer on their services and not only on the streamlit server
- Explore more ways to optimize and sanatize prompts
- Research and develop genetic algorithms to optimizate and choose from a pool of prompts
- Develop AI to grade optimized prompts to compare different prompts
- Implementation as a browser extension
