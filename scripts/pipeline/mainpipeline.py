from . import contentsafety, grammar, chatmodel, vagueprompt

def optimizted_prompt(prompt):
    returnmes = {}

    # grammar check will happen here
    corrected_prompt = prompt
    returnmes["log"] = f"grammar log"
    returnmes["prompt"] = corrected_prompt

    harm = contentsafety.safety_check(corrected_prompt)

    if harm >= 4:
        returnmes["log"] += f" | Content is not safe Level: {harm}"
        returnmes["harm"] = 1
        return returnmes
    
    # other operations will take place here
    returnmes["harm"] = 0
    vague_check = vagueprompt.analyze_prompt(corrected_prompt)
    returnmes["vague"] =  vague_check["status"] == "vague"
    
    return returnmes