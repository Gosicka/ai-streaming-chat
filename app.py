import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="Chat")
st.title("Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("输入消息")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    def iter_chunks():
        with requests.post(
            API_URL,
            json={"message": prompt},
            stream=True,
            timeout=120,
        ) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    yield chunk

    with st.chat_message("assistant"):
        reply = st.write_stream(iter_chunks())
    st.session_state.messages.append({"role": "assistant", "content": reply or ""})
