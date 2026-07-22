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
        # st.write_stream expects a generator that yields text pieces
        def stream_response():
            from llm_client import client, SYSTEM_PROMPT
            from google.genai import types as genai_types
            from tools import calculator, web_search, read_file, run_python_code, read_pdf, search_knowledge_base

            st.session_state.history.append(
                genai_types.Content(role="user", parts=[genai_types.Part(text=user_input)])
            )

            stream = client.models.generate_content_stream(
                model="gemini-3.1-flash-lite",
                config=genai_types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    tools=[calculator, web_search, read_file, run_python_code, read_pdf, search_knowledge_base]
                ),
                contents=st.session_state.history
            )
            full_text = ""
            chunk_count = 0
            for chunk in stream:
                chunk_count += 1
                print(f"CHUNK {chunk_count}: text={chunk.text!r}")
                if chunk.text:
                    full_text += chunk.text
                    yield chunk.text

            print(f"TOTAL CHUNKS: {chunk_count}, FULL TEXT LENGTH: {len(full_text)}")

            st.session_state.history.append(
                genai_types.Content(role="model", parts=[genai_types.Part(text=full_text)])
            )
            st.session_state._last_reply = full_text

    reply = st.write_stream(stream_response())

    save_message("model", st.session_state._last_reply)
    st.session_state.display_messages.append(("user", user_input))
    st.session_state.display_messages.append(("model", st.session_state._last_reply))