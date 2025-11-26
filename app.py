import asyncio

# Ensure an event loop exists for Streamlit's ScriptRunner thread
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from dotenv import load_dotenv
from configs.config import EPHE_PATH
from views import home, form, chat
import os
import traceback
import streamlit as st
import swisseph as swe

# Load environment variables
load_dotenv()

try:
    swe.set_ephe_path(os.path.abspath(EPHE_PATH))

    # Page Config
    st.set_page_config(page_title="DirectionAI", page_icon=":star:")

    # Session state management
    if "page" not in st.session_state:
        st.session_state.page = "home" # default page
    if "username" not in st.session_state:
        st.session_state.user_type = None
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_json" not in st.session_state:
        st.session_state.user_json = None
    if "qa_chain" not in st.session_state:
        st.session_state.qa_chain = None
    if "birth_chart" not in st.session_state:
        st.session_state.birth_chart = None

    # Router
    if st.session_state.page == "home":
        home.render_home()
    elif st.session_state.page == "register":
        form.render_form_page()
    elif st.session_state.page == "chat":
        chat.render_chat_page()
except Exception as e:
    st.error("500 Internal Server Error: Something went wrong!", icon="🚨")
    print(f"Exception: {e}\nTraceback:")
    traceback.print_exc()