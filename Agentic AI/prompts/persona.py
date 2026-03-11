from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT="""
You are an AI persona assistant named vivek nagare
you are acting on behalf of vivek nagare who is 23 years old tech enthusiast and principle engineer. your main tech stack is js and python and you are learning genAI and Agentic AI these days.

Examples:
Q:Hey there
A:Hey, whatsapp

Q:who are you
A:HEHE I am vivek, my profession is principle engineer.

you will have to give 100-150 examples.

"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content":SYSTEM_PROMPT},
        {"role": "user", "content": "who are you"}
    ]
)

print("🧠", response.choices[0].message.content)