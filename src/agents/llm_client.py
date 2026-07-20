"""
Shared Groq LLM client for judge agents.
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_client = None
MODEL_NAME = "llama-3.1-8b-instant"


def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found. Check your .env file.")
        _client = Groq(api_key=api_key)
    return _client


def call_judge(system_prompt, user_prompt):
    """
    Sends a judge prompt to the LLM and parses a JSON response.

    Returns:
        dict: parsed JSON from the model's response
    """
    client = get_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    return json.loads(content)