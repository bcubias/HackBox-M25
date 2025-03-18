from . import contentsafety, grammar, chatmodel

def optimizted_prompt(prompt):
    returnmes = {}

    # grammar check will happen here
    corrected_prompt = prompt
    returnmes["log"] = f"grammar log"

    harm = contentsafety.safety_check(corrected_prompt)

    if harm >= 4:
        returnmes["log"] += f" | Content is not safe Level: {harm}"
        returnmes["harm"] = 1
    else:
        # other operations will take place here
        returnmes["harm"] = 0
        print("prompt")
    
    return returnmes