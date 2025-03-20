from . import contentsafety, grammar, chatmodel, vagueprompt

def optimizted_prompt(prompt):
    message = {}
    logs = ""

    # int varibles
    message["log"] = f"Previous Prompt: {prompt}"
    message["prompt"] = prompt
    message["warning"] = "none"

    harm = contentsafety.safety_check(prompt)

    if harm >= 4:
        logs += f"\nContent is not safe Level: {harm}"
        message["warning"] = "harm"

        print("harmful Message detected")
        
    vague_check = vagueprompt.analyze_prompt(prompt)
    
    if vague_check["status"] == "vague":
        message["warning"] = "vague"
        logs += f"\nVague Message detected"
    else:
        response = chatmodel.chat_with_gpt4o(prompt, "optimize")
        message["prompt"] = response
        message["log"] += f"\nTurns Into: {response}" 
        print(response)

    message["log"] += logs    
    
    return message