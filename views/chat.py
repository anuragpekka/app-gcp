from utils.memory import save_memory_to_file
import streamlit as st
import time

def render_chat_page():
    # ------------------------------
    # Chat Page
    # ------------------------------
    with st.sidebar:
        st.markdown("**Birth Details:**")
        st.markdown(f"Date: *{st.session_state.user_json["day"]}/{st.session_state.user_json["month"]}/{st.session_state.user_json["year"]}*")
        st.markdown(f"Time: *{st.session_state.user_json["hour"]}:{st.session_state.user_json["min"]}:{st.session_state.user_json["sec"]}*")
        st.markdown(f"Place: *{st.session_state.user_json["place"]}*")
        
        if st.button("Logout"):
        # Back button
            # Save memory
            save_memory_to_file(st.session_state.session_id, st.session_state.qa_chain.memory)
            
            st.session_state.user_json = None
            st.session_state.page = "home"
            st.session_state.birth_chart = None
            st.session_state.messages = []
            st.session_state.session_id = None
            st.session_state.qa_chain = None
            st.rerun()

    st.subheader(":star: DirectionAI")
    welcome_msg = f"Namaste! {st.session_state.user_json["name"].split()[0]} ji. Kripya apna sawal puchiye.😊"
    with st.chat_message("assistant"):
        st.markdown(welcome_msg)

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if user_input := st.chat_input("Ask me your future..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            with st.spinner("Thinking..."):
                result = st.session_state.qa_chain.invoke({"question": user_input, "json": st.session_state.birth_chart})

        answer = result["answer"]
        answer = eval(answer)
        for sentence in answer:
            st.session_state.messages.append({"role": "assistant", "content": sentence})
            with st.chat_message("assistant"):
                st.markdown(sentence)
                with st.spinner("Replying..."):
                    time.sleep(4)
