from utils.memory import load_memory_from_file
from chains.rag_chain import build_chain
from configs.config import USER_DIR, USER_FILE
import streamlit as st
import json
import os


def load_users():
    user_filepath = os.path.join(USER_DIR, USER_FILE)
    user_filepath = os.path.abspath(user_filepath)
    if not os.path.exists(user_filepath):
        print(f">>> No file {user_filepath} to load")
        return {}
    with open(user_filepath, "r") as f:
        print(f">>> Loading file {user_filepath}")
        return json.load(f)

def render_home():
    st.title(":star: DirectionAI")

    with st.form("login_form"):
        users = load_users()
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if username in users and users[username]["password"] == password:
                user = users[username]
                st.success("✅ Login successful!")
                st.session_state.session_id = username
                st.session_state.page = "chat"
                st.session_state.birth_chart = user["birth_chart"]
                st.session_state.user_json = {
                    "name": user["name"],  "place": user["place"],
                    "day": user["day"], "month": user["month"], "year": user["year"],
                    "hour": user["hour"], "min": user["minute"], "sec": user["second"]
                    }
                memory, session_chats = load_memory_from_file(st.session_state.session_id)
                st.session_state.qa_chain = build_chain(memory)
                st.session_state.messages = session_chats

                st.rerun()
            else:
                st.error("❌ Wrong username or password")

    with st.sidebar:
        st.markdown("*New user?*")
        if st.button("Register"):
            st.session_state.page = "register"
            st.rerun()
