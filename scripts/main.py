import streamlit as st
from chat import page_config

st.set_page_config(layout="wide")

logo = "assets/prompterAIFinal.png"
icon = "assets/BrainFinal.png"

logo_path = "assets/prompterai-logo-optimized.png"
st.logo(logo, size="large", icon_image=icon)

if "pages" not in st.session_state:
    st.session_state.pages = {}

if "current_page" not in st.session_state:
    st.session_state.current_page = None

if "count" not in st.session_state:
    st.session_state.count = 0

if "open_settings" not in st.session_state:
    st.session_state.open_settings = None

if "running" not in st.session_state:
    st.session_state.running = False

if "show_clear_dialog" not in st.session_state:
    st.session_state.show_clear_dialog = False

if "dialog_was_open" not in st.session_state:
    st.session_state.dialog_was_open = False

if "rename_mode" not in st.session_state:
    st.session_state.rename_mode = {}

def reset_dialog_state():
    st.session_state.show_clear_dialog = False
    st.session_state.dialog_was_open = False

def add_page():
    new_id = f"Session {st.session_state.count + 1}"
    st.session_state.count += 1
    st.session_state.pages[new_id] = [[], []]
    st.session_state.current_page = new_id
    st.session_state.open_settings = None
    st.session_state.running = False

def delete_page(page):
    if page is None:
        return

    if st.session_state.current_page == page:
        st.session_state.current_page = None

    st.session_state.rename_mode.pop(page, None)
    del st.session_state.pages[page]
    st.session_state.running = False

    if len(st.session_state.pages) == 0:
        st.session_state.count = 0 

def toggle_settings(page):
    for key in st.session_state.rename_mode:
        st.session_state.rename_mode[key] = False
    if st.session_state.open_settings != page:
        st.session_state.open_settings = page
    else:
        st.session_state.open_settings = None

def close_dialog():
    st.session_state.show_clear_dialog = False
    st.session_state.dialog_was_open = False

# Function to select active session(page)
def select_page(page):
    st.session_state.current_page = page

def rename_session(old_name):
    new_name = st.session_state.get(f"rename_value_{old_name}", "").strip()
    if new_name and new_name != old_name and new_name not in st.session_state.pages:
        st.session_state.pages[new_name] = st.session_state.pages.pop(old_name)
        if st.session_state.current_page == old_name:
            st.session_state.current_page = new_name
        st.session_state.rename_mode[new_name] = False
        st.session_state.open_settings = None
        st.rerun()

with st.sidebar:
    col1, col2, col3 = st.columns([3, 1, 1])  

    with col1:
        st.title("Sessions")

    with col2:
        st.write("")
        st.button("", help="Add page", icon=":material/add:", on_click=add_page, disabled=st.session_state.running)
    with col3:
        st.write("")
        st.button(
            "", 
            help="Delete all sessions", 
            icon=":material/delete:", 
            key="delete_all_sessions",
            on_click=lambda: setattr(st.session_state, "show_clear_dialog", True),
            disabled=len(st.session_state.pages) == 0 or st.session_state.running
        )

    # Highlighting active session
    for page in st.session_state.pages:
        is_active = page == st.session_state.current_page
        button_type = "primary" if is_active else "secondary"

        col1, col2 = st.columns([4, 1])

        with col1:
            st.button(page, help=f"Switch to {page}", use_container_width=True, type=button_type, 
                      on_click=select_page, args=(page,), disabled=st.session_state.running)

        with col2:
            st.button(":material/more_horiz:", help="More options", key=f"more_btn_{page}", 
                      on_click=toggle_settings, args=(page,), disabled=st.session_state.running)
        
        if st.session_state.open_settings == page:
            with st.expander(":material/settings: Options", expanded=True):
                if not st.session_state.rename_mode.get(page, False):
                    if st.button(":material/edit: Rename", key=f"rename_btn_{page}"):
                        st.session_state.rename_mode[page] = True
                        st.rerun()
                else:
                    with st.form(key=f"rename_form_{page}", clear_on_submit=False):
                        new_name = st.text_input("Rename session:", value=page, key=f"rename_value_{page}", label_visibility="collapsed")
                        col_save, col_cancel = st.columns(2)
                        submit = col_save.form_submit_button(":material/check: Save")
                        cancel = col_cancel.form_submit_button(":material/close: Cancel")
                        if submit:
                            rename_session(page)
                        if cancel:
                            st.session_state.rename_mode[page] = False
                            st.rerun()

                st.button(":material/delete: Delete Session", key=f"delete_btn_{page}", on_click=delete_page, args=(page,), disabled=st.session_state.running)

@st.dialog("Confirm Deletion")
def confirm_clear_dialog():
    st.session_state.dialog_was_open = True 

    st.markdown("""
        <style>
            .dialog-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                font-size: 18px;
            </style>
        </style>
        <div class="dialog-container">
            <h3>Are you sure you want to delete all sessions?</h3>
            <p><b>This action cannot be undone.</b></p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3.5, 1])

    if col1.button(":material/check: Confirm", key="confirm_clear_all"):
        st.session_state.pages.clear()
        st.session_state.current_page = None
        st.session_state.count = 0
        st.session_state.open_settings = None
        reset_dialog_state()
        st.rerun()

    if col2.button(":material/close: Cancel", key="cancel_clear_all"):
        reset_dialog_state()
        st.rerun()

if st.session_state.show_clear_dialog:
    confirm_clear_dialog()
    st.session_state.show_clear_dialog = False

if st.session_state.current_page:
    page_config(st.session_state.current_page)
else:
    st.info("No active sessions. Click the '+' or select a session to start chatting.")