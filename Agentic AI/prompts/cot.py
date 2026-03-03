from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
SYSTEM_PROMPT=""" 
You're an expert AI Assistant in resolving user queries using chain of thoughts.
you work on START, PLAN and OUTPUT steps.
you need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.
Rules:
- Strictly follow the given JSON output format
- Only run one step at a Time.
- The Sequence of steps is START (where user gives an input), PLAN(That can be multiple times) and finally OUTPUT (which is going to displayed to the user).

Output JSON format:
{"step: "START" | "PLAN" | "OUTPUT", "content": "string"}

Example:
START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN: {"Step": "PLAN", "content": "Seems like user is interested in Maths problem"}
PLAN: {"Step": "PLAN", "content": "Looking at the problem we should solve it using BODMAS method"}
PLAN: {"Step": "PLAN", "content": "Yes, the BODMAS is correct thing to be done here"}
PLAN: {"Step": "PLAN", "content": "First we multiply 3 * 5 which is 15"}
PLAN: {"Step": "PLAN", "content": "Now the new equation is 2 + 15 / 10"}
PLAN: {"Step": "PLAN", "content": "Now we must perform the division 15 / 10 which is equal to 1.5"}
PLAN: {"Step": "PLAN", "content": "Now the new equation is 2 + 1.5"}
PLAN: {"Step": "PLAN", "content": "Now finally perform the addition so,  2 + 1.5 will give me 3.5"}
PLAN: {"Step": "PLAN", "content": "Great! we have solved the problem and finally left with 3.5 which is the answer"}
PLAN: {"Step": "OUTPUT", "content": "3.5"}
"""

#cmd + shft + p -> to toggle word wrap, for wrapping the big sentence

response = client.chat.completions.create(
    model = "gemini-2.5-flash", 
    response_format={"type":"json_object"},
    messages=[
        {"role" : "system", "content": SYSTEM_PROMPT},
        {"role" : "user", "content" : "write a code to add n numbers in python"},
        {"role": "assistant", "content": json.dumps({"step": "PLAN",
        "content": "The user wants Python code to add 'n' numbers. I should define a function that takes an arbitrary number of arguments or a list of numbers and returns their sum."})},
        {"role": "assistant", "content": json.dumps({"step": "PLAN", "content": "The user wants Python code to add 'n' numbers. I will create a function that takes a variable number of arguments using `*args` or a list and then uses the built-in `sum()` function for an efficient and Pythonic solution. I'll provide an example usage"})}
    ]
)
print(response.choices[0].message.content)



