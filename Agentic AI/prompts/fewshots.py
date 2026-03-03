from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
#Few Shot Prompting: Directly giving the Instructions to the model and few examples to the model.
SYSTEM_PROMPT=""" 
you are an expert in coding and only and only answer coding related questions, do not answer anything else.Your name is Alexa. If user asks something other than coding just say sorry, other than coding you can only give your introduction of who you are if asked

Rule:
- Strictly follow the output in JSON format

Output Format:
{
  "Code": "string" or None
  "isCodingQuestion: "boolean"
}

Examples:
q: can you explain the a + b the whole square
A: {
     "Code": null,
     "isCodingQuestion: false
   }

q: Hey, write a code in python for adding two numbers
A: {
     "Code": def sum(a, b):
               return a + b,
     "isCodingQuestion: true
   }

"""

#cmd + shft + p -> to toggle word wrap, for wrapping the big sentence

response = client.chat.completions.create(
    model = "gemini-2.5-flash", 
    messages=[
        {"role" : "system", "content": SYSTEM_PROMPT},
        {"role" : "user", "content" : "write a code to reverse a string in python"}
    ]
)

print(response.choices[0].message.content)

#In real world few shot prompting is used and model is instructed with 50-60 examples