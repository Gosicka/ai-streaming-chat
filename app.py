import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(page_title="Chat")
st.title("Chat")

api_key = os.environ.get("DEEPSEEK_API_KEY")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if not api_key:
    st.error("未找到环境变量 DEEPSEEK_API_KEY。请在项目根目录的 .env 中配置后重启应用。")

prompt = st.chat_input("输入消息", disabled=not api_key)
if prompt and api_key:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    def iter_chunks(message: str):
        stream = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": message}],
            stream=True,
        )
        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    with st.chat_message("assistant"):
        reply = st.write_stream(iter_chunks(prompt))
    st.session_state.messages.append({"role": "assistant", "content": reply or ""})
