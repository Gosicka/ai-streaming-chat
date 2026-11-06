"""基于 Streamlit 的 DeepSeek 流式聊天应用。"""

import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MAX_INPUT_CHARS = 1000
MAX_OUTPUT_TOKENS = 1024
SESSION_CHAR_LIMIT = 30000
MODEL_NAME = "deepseek-chat"
API_BASE_URL = "https://api.deepseek.com"


def stream_reply(client: OpenAI, messages: list[dict[str, str]]):
    """逐块返回模型增量文本，供界面流式渲染。"""
    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        stream=True,
        max_tokens=MAX_OUTPUT_TOKENS,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


st.set_page_config(page_title="AI 流式聊天")
st.title("AI 流式聊天")

api_key = os.environ.get("DEEPSEEK_API_KEY")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_chars_used" not in st.session_state:
    st.session_state.total_chars_used = 0

over_limit = st.session_state.total_chars_used >= SESSION_CHAR_LIMIT

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

usage = st.empty()
usage.caption(
    f"本会话已使用 {st.session_state.total_chars_used} / {SESSION_CHAR_LIMIT} 个字符"
)

if not api_key:
    st.error("未找到环境变量 DEEPSEEK_API_KEY。请在项目根目录的 .env 中配置后重启应用。")

if over_limit:
    st.warning(
        f"本会话累计已达到 {SESSION_CHAR_LIMIT} 个字符的上限，无法继续发送。请刷新页面开始新会话。"
    )

prompt = st.chat_input(
    "输入消息",
    max_chars=MAX_INPUT_CHARS,
    disabled=not api_key or over_limit,
)

if over_limit or not api_key:
    st.stop()

client = OpenAI(api_key=api_key, base_url=API_BASE_URL)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        reply = st.write_stream(stream_reply(client, st.session_state.messages))
    reply = reply or ""
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.total_chars_used += len(prompt) + len(reply)
    usage.caption(
        f"本会话已使用 {st.session_state.total_chars_used} / {SESSION_CHAR_LIMIT} 个字符"
    )
    if st.session_state.total_chars_used >= SESSION_CHAR_LIMIT:
        st.rerun()
