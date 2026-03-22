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

message_history = [
    {"role" : "system", "content": SYSTEM_PROMPT}
]

user_query = input("👉🏻 ")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type":"json_object"},
        messages=message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role":"assistant", "content":raw_result})

    parse_result = json.loads(raw_result)

    if(parse_result.get("step") == "START"):
        print("🔥", parse_result.get("content"))
        continue

    if(parse_result.get("step") == "PLAN"):
        print("🧠", parse_result.get("content"))
        continue

    if(parse_result.get("step") == "OUTPUT"):
        print("🤖", parse_result.get("content"))
        break



#cmd + shft + p -> to toggle word wrap, for wrapping the big sentence





