import streamlit as st
from llm_client import ask
from memory_db import init_db, save_message, load_all_messages
from google.genai import types

st.set_page_config(page_title="DevBuddy AI", page_icon="🤖")
st.title("🤖 DevBuddy AI")

init_db()

# Load history into Streamlit's session state (persists across reruns within one browser session)
if "history" not in st.session_state:
    saved_messages = load_all_messages()
    st.session_state.history = []
    for role, content in saved_messages:
        st.session_state.history.append(types.Content(role=role, parts=[types.Part(text=content)]))
    st.session_state.display_messages = saved_messages  # for showing in the UI

# Display past messages
for role, content in st.session_state.display_messages:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.write(content)

# Chat input box
user_input = st.chat_input("Ask DevBuddy something...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    save_message("user", user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply, st.session_state.history = ask(user_input, st.session_state.history)
            st.write(reply)

    save_message("model", reply)
    st.session_state.display_messages.append(("user", user_input))
    st.session_state.display_messages.append(("model", reply))