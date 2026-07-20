"""
Quick sanity check that the Groq API key works before touching agent code.
"""

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # reads .env and loads GROQ_API_KEY into environment

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "Reply with exactly one word: 'working'"}
    ],
)

print("Groq response:", response.choices[0].message.content)