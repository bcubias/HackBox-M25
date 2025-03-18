import streamlit as st
from pipeline.mainpipeline import optimizted_prompt

def page_config(page_id):
    """
    Configures the chat page for a given session.
    """
    st.title(page_id)

    col1, col2 = st.columns([5, 2])

    # ✅ Take User Input
    if prompt := st.chat_input("Enter your message:", max_chars=st.session_state.char_limit):
        # ✅ Step 1: Optimize User Prompt (includes grammar check)
        optimized = optimizted_prompt(prompt)

        # ✅ Step 2: Log Optimized Input
        st.session_state.pages[page_id][0].append({"role": "user", "content": optimized["prompt"]})

        # ✅ Step 3: Display AI Logs
        st.session_state.pages[page_id][1].append(optimized["log"])

    # Display Messages & Logs
    with col1:
        for message in st.session_state.pages[page_id][0]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    with col2:
        for log in st.session_state.pages[page_id][1]:
            st.chat_message("ai").write(log)
            st.markdown("---")