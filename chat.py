import streamlit as st
from streamlit_float import *

def page_config(page_id):
    # Page layout
    st.title(page_id)
    col1, col2 = st.columns([5, 2])

    with col1:        
        # Display messages
        for message in st.session_state.pages[page_id][0]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input and default prompt
        if prompt := st.chat_input("What is up?"):
            # Add user input to messages
            st.chat_message("user").markdown(prompt)
            st.session_state.pages[page_id][0].append({"role": "user", "content": prompt})

            # Get response and log changes
            response = f"Echo: {prompt}"
            st.session_state.pages[page_id][1].append(prompt)

            # Add response to messages
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.pages[page_id][0].append({"role": "assistant", "content": response})

    with col2:
        # Display logs
        for log in st.session_state.pages[page_id][1]:
            st.write(log)