import streamlit as st
from chat import page_config
from PIL import Image

# Load the image
image_path = "assets/prompterai-transparent.png"
image = Image.open(image_path)

# Auto-crop to remove white space
image = image.crop(image.getbbox())  

# Resize to 320x40
new_size = (320, 40)  
resized_image = image.resize(new_size, Image.LANCZOS)

# Save optimized image
resized_logo_path = "assets/prompterai-logo-optimized.png"
resized_image.save(resized_logo_path, "PNG")

logo = "assets/prompterai-transparent.png"
icon = "assets/transparent-brain.PNG"

logo_path = "assets/prompterai-logo-optimized.png"
st.logo(logo_path, size="large", icon_image=icon)

if "pages" not in st.session_state:
    st.session_state.pages = {}

if "current_page" not in st.session_state:
    st.session_state.current_page = None

if "count" not in st.session_state:
    st.session_state.count = 0

if "char_limit" not in st.session_state:
    st.session_state.char_limit = 4096

if "open_settings" not in st.session_state:
    st.session_state.open_settings = None

def add_page():
    new_id = f"Session {st.session_state.count + 1}"
    st.session_state.count += 1
    st.session_state.pages[new_id] = [[], []]
    st.session_state.current_page = new_id

def delete_page(page):
    if page == None:
        return

    if st.session_state.current_page:        
        st.session_state.current_page = None

    del st.session_state.pages[page]

def toggle_settings(page):
    if st.session_state.open_settings == None or st.session_state.open_settings != page:
        st.session_state.open_settings = page
    else:
        st.session_state.open_settings = None

# Function to select active session(page)
def select_page(page):
    st.session_state.current_page = page

with st.sidebar:

    col1, col2, col3 = st.columns([3, 1, 1])  

    with col1:
        st.title("Sessions")

    with col2:
        st.write("")
        st.button("", help="Add page", icon = ':material/add:', on_click=add_page)

    with col3:
        st.write("")
        st.button("", help="Delete page", icon = ':material/delete:', on_click=delete_page, args=(st.session_state.current_page,))

    st.session_state.char_limit = st.slider("Max Character Limit", 0, 4096, 4096)

    # Highligting active session
    for page in st.session_state.pages:
        is_active = page == st.session_state.current_page
        button_type = "primary" if is_active else "secondary"

        col1, col2 = st.columns([4, 1])

        with col1:
            st.button(page, help=f"Switch to {page}", use_container_width=True, type=button_type, on_click=select_page, args=(page,))

        with col2:
            st.button(":material/more_horiz:", help="More options", key=f"more_btn_{page}", on_click=toggle_settings, args=(page,))
        
        if st.session_state.open_settings == page:
            # st.button(":material/edit: Rename", key=f"rename_btn_{page}")
            st.button(":material/delete: Remove", key=f"delete_btn_{page}" , on_click=delete_page, args=(page,))
                
if st.session_state.current_page:
    page_config(st.session_state.current_page)
else:
    st.info("No active sessions. Click the '+' or selct a session to start chatting.")