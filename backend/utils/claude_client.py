import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key or api_key == "your_key_here":
            raise ValueError("ANTHROPIC_API_KEY not set in .env file")
        _client = anthropic.Anthropic(api_key=api_key)
    return _client

def call_claude(prompt: str, system: str = "", max_tokens: int = 4096) -> str:
    client = get_client()
    messages = [{"role": "user", "content": prompt}]
    kwargs = {"model": "claude-sonnet-4-5", "max_tokens": max_tokens, "messages": messages}
    if system:
        kwargs["system"] = system
    response = client.messages.create(**kwargs)
    return response.content[0].text
