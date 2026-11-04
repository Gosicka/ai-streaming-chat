import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)


class ChatRequest(BaseModel):
    message: str


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


@app.post("/chat")
def chat(body: ChatRequest) -> StreamingResponse:
    return StreamingResponse(
        iter_chunks(body.message),
        media_type="text/plain; charset=utf-8",
    )
