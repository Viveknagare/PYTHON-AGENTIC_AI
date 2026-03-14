from fastapi import FastAPI,Body
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = "you are an expert in coding and only and only answer coding related questions, do not answer anything else.Your name is Alexa. If user asks something other than coding just say sorry, other than coding you can only give your introduction of who you are if asked"


@app.post("/chat")
def function(message:str = Body(..., description="user input")):
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content":SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

