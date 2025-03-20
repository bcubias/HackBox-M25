from . import contentsafety, chatmodel, vagueprompt

def optimizted_prompt(prompt, status):
    message = {}
    logs = ""

    # int varibles
    message["log"] = f"Previous Prompt: {prompt}"
    message["prompt"] = prompt
    message["warning"] = "none"

    status.write("Checking for harmful content...")
    harm = contentsafety.safety_check(prompt)

    if harm >= 4:
        logs += f"\nContent is not safe Level: {harm}"
        message["warning"] = "harm"
        message["log"] += logs
        return message
        
    status.write("Checking for vague content...")    
    vague_check = vagueprompt.analyze_prompt(prompt)
    
    if vague_check["status"] == "vague":
        message["warning"] = "vague"
        logs += f"\nVague Message detected"
    else:
        status.write("Optimizing prompt...")
        response = chatmodel.chat_with_gpt4o(prompt, "optimize")
        message["prompt"] = response
        message["log"] += f"\nTurns Into: {response}" 
        print(response)

    message["log"] += logs    
    
    return message