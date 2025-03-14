import streamlit as st
from chat import page_config

if "pages" not in st.session_state:
    st.session_state.pages = {}

if "current_page" not in st.session_state:
    st.session_state.current_page = None

if "count" not in st.session_state:
    st.session_state.count = 0

if "char_limit" not in st.session_state:
    st.session_state.char_limit = 4096

def add_page():
    new_id = f"Session {st.session_state.count + 1}"
    st.session_state.count += 1
    st.session_state.pages[new_id] = [[], []]
    st.session_state.current_page = new_id

def delete_page():
    if st.session_state.current_page:
        del st.session_state.pages[st.session_state.current_page]
        st.session_state.current_page = None

with st.sidebar:
    col1, col2, col3 = st.columns([3, 1, 1])  

    with col1:
        st.title("Sessions")

    with col2:
        st.write("")
        st.button("", help="add page", icon = ':material/add:', on_click=add_page)

    with col3:
        st.write("")
        st.button("", help="delete page", icon = ':material/delete:', on_click=delete_page)

    st.session_state.char_limit = st.slider("Max Character Limit", 0, 4096, 4096)

    for page in st.session_state.pages:
        if st.button(page, help=f"{page}", use_container_width=True, type="secondary"):
            st.session_state.current_page = page

if not st.session_state.pages:
    st.info("No active sessions. Click the '+' to start one!")
            
if st.session_state.current_page:
    # Use the chat layout from chat.py
    page_config(st.session_state.current_page)

    
