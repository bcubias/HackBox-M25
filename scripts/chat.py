import streamlit as st
from pipeline.mainpipeline import optimizted_prompt

def page_config(page_id):
    # Page layout
    st.title(page_id)

    col1, col2 = st.columns([5, 2])

    # Chat input 
    if prompt := st.chat_input("What is up?", max_chars=st.session_state.char_limit):
        # Log user input
        st.session_state.pages[page_id][0].append({"role": "user", "content": prompt})

        # Get and log response and change
        message = optimizted_prompt(prompt)
        response = message["prompt"]

        st.session_state.pages[page_id][1].append(message["log"])
        st.session_state.pages[page_id][0].append({"role": "ai", "content": response})

    # Display chat messages
    with col1: 
        for message in st.session_state.pages[page_id][0]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Display logs
    with col2:
        for log in st.session_state.pages[page_id][1]:
            st.chat_message("ai").write(log)
            st.markdown("---")