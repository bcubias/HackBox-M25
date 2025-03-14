import streamlit as st
from chat import page_config

if "pages" not in st.session_state:
    st.session_state.pages = {}

if "current_page" not in st.session_state:
    st.session_state.current_page = None
        
with st.sidebar:
    col1, col2 = st.columns([3, 1])  

    with col1:
        st.title("Sessions")

    with col2:
        st.write("")
        add = st.button("", help="add page", icon = ':material/add:')

    for page in st.session_state.pages:
        if st.button(page, help=f"{page}", use_container_width=True):
            st.session_state.current_page = page

    if add:
        new_id = f"Session {len(st.session_state.pages) + 1}"
        st.session_state.pages[new_id] = [[], []]
        st.session_state.current_page = new_id
        

    
