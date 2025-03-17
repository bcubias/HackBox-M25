from . import contentsafety
from .chatmodel import chat_with_gpt4o 

def optimizted_prompt(prompt):
    returnmes = {}

    response = chat_with_gpt4o(prompt)

    harm = contentsafety.safety_check(response)

    returnmes["prompt"] = response
    returnmes["log"] = f"Content is safe"

    if harm >= 4:
        returnmes["log"] = f"Content is not safe Level: {harm}"
    
    return returnmes