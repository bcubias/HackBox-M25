import streamlit as st
from streamlit_float import *

def page_config(page_id, ip_message, ip_log):
    # Page layout
    st.set_page_config(f"{page_id}", layout="wide")
    col1, col2 = st.columns([5, 2])

    with col1:
        # Initialize Messages and Logs array
        if "messages" not in st.session_state:
            st.session_state.messages = [ip_message]
        if "logs" not in st.session_state:
            st.session_state.logs = [ip_log]

        # Display messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input and default prompt
        if prompt := st.chat_input("What is up?"):
            # Add user input to messages
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Get response and log changes
            response = f"Echo: {prompt}"
            st.session_state.logs.append(prompt)

            # Add response to messages
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    with col2:
        # Display logs
        for log in st.session_state.logs:
            st.write(log)