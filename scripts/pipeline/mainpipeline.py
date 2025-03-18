from . import contentsafety, grammar, chatmodel

def optimizted_prompt(prompt):
    returnmes = {}

    # ✅ Step 1: Perform Grammar Check using GPT-4o
    corrected_prompt, grammar_log = grammar.grammar_check(prompt)

    # ✅ Step 2: Run Content Safety Check
    harm = contentsafety.safety_check(corrected_prompt)

    # ✅ Step 3: Generate AI Response using GPT-4o
    ai_response = chatmodel.chat_with_gpt4o(corrected_prompt)

    # ✅ Step 4: Return AI Response and Logs
    returnmes["prompt"] = ai_response
    returnmes["log"] = f"{grammar_log} | Content is safe"

    if harm >= 4:
        returnmes["log"] += f" | Content is not safe Level: {harm}"
    
    return returnmes