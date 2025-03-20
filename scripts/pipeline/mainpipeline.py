from . import contentsafety, grammar, chatmodel

def optimizted_prompt(prompt):
    returnmes = {}

    # grammar check will happen here
    corrected_prompt = prompt
    returnmes["log"] = ""
    returnmes["prompt"] = ""
    returnmes["harm"] = 0
    returnmes["vague"] = 0
    returnmes["prevPrompt"] = corrected_prompt
    

    harm = contentsafety.safety_check(corrected_prompt)

    if harm >= 4:
        returnmes["log"] += f" | Content is not safe Level: {harm}"
        print("harmful Message detected")
        returnmes["harm"] = 1

    else:
        
        response = chatmodel.chat_with_gpt4o(corrected_prompt, "optimize")
        returnmes["prompt"] = response
        print(response)
    
    return returnmes