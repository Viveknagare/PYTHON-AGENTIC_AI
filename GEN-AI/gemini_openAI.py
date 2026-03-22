from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model = "gemini-2.5-flash", 
    messages=[
        {"role" : "system", "content": "you are an expert in maths and only and only answer maths related questions, and if the query is not related to maths just say sorry and dont answer"},
        {"role" : "user", "content" : "hey can you help me solve a + b the whole square"}
    ]
)

print(response.choices[0].message.content)