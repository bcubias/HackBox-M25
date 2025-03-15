from . import contentsafety

def optimizted_prompt(prompt):
    returnmes = {}
    returnmes["prompt"] = prompt

    harm = contentsafety.safety_check(prompt)
    returnmes["log"] = f"Content is safe"

    if harm >= 4:
        returnmes["log"] = f"Content is not safe Leavel: {harm}"
    
    return returnmes
