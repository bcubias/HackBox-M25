import streamlit as st
from chat import page_config
import pathlib

# Load CSS File
def load_css(file_path):
    """Loads a CSS file to style the app."""
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path("assets/styles.css")
load_css(css_path)

# Header and Title
st.markdown("""
<div class="header-container">
     <span class="header-title">PrompterAI</span>
</div>
""", unsafe_allow_html=True)

# Initialize session state variables
def init_session_state():
    """Ensures all required session state variables are initialized."""
    defaults = {
        "pages": {},               # Stores session pages
        "current_page": None,      # Tracks the currently selected session
        "count": 0,                # Keeps track of the number of sessions
        "show_clear_dialog": False, # Controls whether the clear-all popup is visible
        "open_menu_page": None,     # Keeps track of which session menu is open
        "rename_mode": {}           # Tracks rename state for each session
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)

st.session_state.setdefault("dark_mode", False)

init_session_state()  # Call to initialize states

def add_page():
    """Creates a new session and sets it as the current page."""
    if st.session_state.show_clear_dialog:
        st.session_state.show_clear_dialog = False  # Close any warning dialogs
    st.session_state.count += 1
    new_id = f"Session {st.session_state.count}"
    st.session_state.pages[new_id] = [[], []]
    st.session_state.current_page = new_id
    st.session_state.rename_mode[new_id] = False  # Ensure rename mode is off

    if "black_mode" not in st.session_state:
        st.session_state.black_mode = False

def rename_session(old_name):
    """Handles renaming a session safely."""
    new_name = st.session_state.get(f"rename_value_{old_name}", "").strip()

    if new_name and new_name != old_name and new_name not in st.session_state.pages:
        # Rename session key in session state
        st.session_state.pages[new_name] = st.session_state.pages.pop(old_name)

        # Update current session if it was renamed
        if st.session_state.current_page == old_name:
            st.session_state.current_page = new_name

        # Close menu & rename input
        st.session_state.open_menu_page = None
        st.session_state.rename_mode[old_name] = False
        st.session_state.rename_mode[new_name] = False  # Reset for new session

        st.experimental_rerun()  # Force UI refresh

# Sidebar UI
with st.sidebar:
    st.markdown("## :material/folder: Sessions") 

    # Buttons for adding and clearing sessions
    col1, col2 = st.columns([1, 5])

    with col1:
        st.button("", help="Add session", icon=":material/add:", on_click=add_page)  

    with col2:
        if st.button("", help="Clear all sessions", icon=":material/delete_sweep:"):
            st.session_state.show_clear_dialog = True  # Show the delete confirmation popup

    st.divider()

    # Display session list with options
    for page in list(st.session_state.pages.keys()):
        col1, col2 = st.columns([4, 1])

        with col1:
            if st.button(page, use_container_width=True, type="primary" if st.session_state.current_page == page else "secondary"):
                st.session_state.current_page = page
                st.experimental_rerun()

        with col2:
            if st.button(":material/more_horiz:", key=f"menu_{page}", help="More options"):
                # Toggle behavior: Clicking the same menu again closes it
                if st.session_state.open_menu_page == page:
                    st.session_state.open_menu_page = None
                else:
                    st.session_state.open_menu_page = page  # Open only the clicked menu
                st.experimental_rerun()

        # Show the options menu if it's open for this session
        if st.session_state.open_menu_page == page:
            with st.expander(":material/settings: Options", expanded=True):
                # Rename Button
                if not st.session_state.rename_mode.get(page, False):
                    if st.button(":material/edit: Rename", key=f"rename_btn_{page}"):
                        st.session_state.rename_mode[page] = True
                        st.experimental_rerun()
                else:
                    new_name = st.text_input(
                        "Rename session:",
                        value=page,
                        key=f"rename_value_{page}"
                    )
                    col_save, col_cancel = st.columns(2)
                    
                    with col_save:
                        if st.button(":material/check: Save", key=f"save_rename_{page}"):
                            rename_session(page)

                    with col_cancel:
                        if st.button(":material/close: Cancel", key=f"cancel_rename_{page}"):
                            st.session_state.rename_mode[page] = False
                            st.experimental_rerun()

                # Delete Session Button
                if st.button(":material/delete: Delete Session", key=f"delete_btn_{page}"):
                    del st.session_state.pages[page]
                    remaining_sessions = list(st.session_state.pages.keys())
                    st.session_state.current_page = remaining_sessions[-1] if remaining_sessions else None
                    st.session_state.open_menu_page = None  # Close menu after deletion
                    st.experimental_rerun()

# Dialog for Confirming "Clear All Sessions"
@st.dialog("Confirm Deletion")
def confirm_clear_dialog():
    """Popup dialog asking the user to confirm deleting all sessions."""
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
            <p>This action <b>cannot be undone</b>.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3.5, 1])

    with col1:
        if st.button(":material/check: Confirm", key="confirm_clear_all"):
            st.session_state.pages.clear()  # Remove all sessions
            st.session_state.current_page = None  # Reset current page
            st.session_state.count = 0  # Reset session count so the next session starts at "Session 1"
            st.session_state.show_clear_dialog = False  # Close dialog
            st.experimental_rerun()

    with col2:
        if st.button(":material/close: Cancel", key="cancel_clear_all"):
            st.session_state.show_clear_dialog = False  # Close dialog
            st.experimental_rerun()

# Show the confirmation dialog if needed
if st.session_state.show_clear_dialog:
    confirm_clear_dialog()
else:
    st.session_state.show_clear_dialog = False  # Reset when closed

if st.session_state.current_page:
    st.set_page_config = page_config(st.session_state.current_page)
