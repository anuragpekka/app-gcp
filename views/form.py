from chains.rag_chain import build_chain
from utils.user_chart import full_birth_chart_details
from configs.config import USER_DIR, USER_FILE
import streamlit as st
import json
import os


def save_user(username, password, name, gender, year, month, day, hour, minute, second, place, birth_chart):
    os.makedirs(USER_DIR, exist_ok=True)
    user_filepath = os.path.join(USER_DIR, USER_FILE)
    user_filepath = os.path.abspath(user_filepath)
    print(f">>> user_filepath={user_filepath}")
    if not os.path.exists(user_filepath):
        print(f">>> {user_filepath} does not exist")
        users = {}
    else:
        print(f">>> opening user_filepath={user_filepath}")
        with open(user_filepath, "r") as f:
            users = json.load(f)

    if username in users:
        return False  # User already exists

    users[username] = {"password": password, "gender": gender, "name": name,
                       "year": year,"month": month, "day": day,
                       "hour": hour, "minute": minute, "second": second,
                       "place": place, "birth_chart": birth_chart
                       }
    with open(user_filepath, "w") as f:
        print(f"Writing user_db file: {user_filepath}")
        json.dump(users, f, indent=2)
    return True


def render_form_page():
    # ------------------------------
    # Home Page (Form)
    # ------------------------------
    st.title(":star: DirectionAI")
    st.markdown("**Register New User** 📝")

    with st.form("user_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        name = st.text_input("Name", "Guest")
        gender = st.selectbox("Gender", ["male", "female"], index=0)
        day = st.number_input("Day", min_value=1, max_value=31, value=1)
        month = st.number_input("Month", min_value=1, max_value=12, value=1)
        year = st.number_input("Year", min_value=1900, max_value=2100, value=1999)
        hour = st.number_input("Hour", min_value=0, max_value=23, value=10)
        minute = st.number_input("Minute", min_value=0, max_value=59, value=10)
        second = st.number_input("Second", min_value=0, max_value=59, value=0)
        place = st.text_input("Place of Birth", "New Delhi,India")
        submitted = st.form_submit_button("Start Chat")

        if submitted:
            astro_json = json.loads(full_birth_chart_details(year,month,day,hour,minute,second,place))
            success = save_user(username,password,name,gender,year,month,day,hour,minute,second,place,astro_json)
            if success:
                st.success("Registration successful! Logging in...")
                st.session_state.page = "chat"
                st.session_state.session_id = username
                st.session_state.birth_chart = astro_json
                st.session_state.messages = []
                st.session_state.qa_chain = build_chain()
                st.session_state.user_json = {
                    "name": name, "day": day, "month": month, "year": year,
                    "hour": hour, "min": minute, "sec": second, "place": place
                    }
                st.rerun()                
            else:
                st.error("❌ Username already exists. Choose another.")
                   
    with st.sidebar:
        if st.button("Back to Login"):
            st.session_state.page = "home"
            st.rerun()
