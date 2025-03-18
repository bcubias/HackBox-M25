import streamlit as st
from pipeline.chatmodel import chat_with_gpt4o
from pipeline.mainpipeline import optimizted_prompt

def page_config(page_id):
    st.title(page_id)

    col1, col2 = st.columns([5, 2])

    # User Input
    if prompt := st.chat_input("Enter your message:", max_chars=st.session_state.char_limit):
        # Optimize Prompt
        optimized = optimizted_prompt(prompt)

        # Save optimized prompt and log
        st.session_state.pages[page_id][0].append({"role": "user", "content": optimized["prompt"]})
        st.session_state.pages[page_id][1].append(optimized["log"])
        
        # Check for harmful content 
        if optimized["harm"]:
            st.session_state.pages[page_id][0].append({"role": "assistant", "content": "Content is not safe, please try again."})
        else:
            response = chat_with_gpt4o(optimized["prompt"])
            st.session_state.pages[page_id][0].append({"role": "assistant", "content": response})
        
    # Display Messages & Logs
    with col1:
        for message in st.session_state.pages[page_id][0]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    with col2:
        for log in st.session_state.pages[page_id][1]:
            st.chat_message("ai").write(log)
            st.markdown("---")