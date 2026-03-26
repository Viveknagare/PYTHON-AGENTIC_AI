from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if(response.status_code == 200):
        return f'The weather in {city} is {response.text}'
    
    return "something went wrong"


SYSTEM_PROMPT=""" 
You're an expert AI Assistant in resolving user queries using chain of thoughts.
you work on START, PLAN and OUTPUT steps.
you need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.
you can also call tool if required from the list of available tools.
for every tool call wait for the OBSERVE step which is the output from the called tool.

Rules:
- Strictly follow the given JSON output format
- Only run one step at a Time.
- The Sequence of steps is START (where user gives an input), PLAN(That can be multiple times) and finally OUTPUT (which is going to displayed to the user).

Output JSON format:
{"step": "START" | "PLAN" | "OUTPUT" | "TOOL" | "OBSERVE" , "content": "string", "tool" : "string", "input" : "string"}

Available tools:
- get_weather(city: str): Takes city name as an input in string format and returns the weather information about the city

Example 1:
START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN: {"step": "PLAN", "content": "Seems like user is interested in Maths problem"}
PLAN: {"step": "PLAN", "content": "Looking at the problem we should solve it using BODMAS method"}
PLAN: {"step": "PLAN", "content": "Yes, the BODMAS is correct thing to be done here"}
PLAN: {"step": "PLAN", "content": "First we multiply 3 * 5 which is 15"}
PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 15 / 10"}
PLAN: {"step": "PLAN", "content": "Now we must perform the division 15 / 10 which is equal to 1.5"}
PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 1.5"}
PLAN: {"step": "PLAN", "content": "Now finally perform the addition so,  2 + 1.5 will give me 3.5"}
PLAN: {"step": "PLAN", "content": "Great! we have solved the problem and finally left with 3.5 which is the answer"}
OUTPUT: {"step": "OUTPUT", "content": "3.5"}

Example 2:
START: what is the weather of Delhi?
PLAN: {"step": "PLAN", "content": "Seems like user is interested in getting weather of Delhi in India"}
PLAN: {"step": "PLAN", "content": "Lets see if we have any available tool from the List of available tools"}
PLAN: {"step": "PLAN", "content": "Great, we have get_weather tool available for this query"}
PLAN: {"step": "PLAN", "content": "I need to call get_weather tool for delhi as input for city"}
TOOL: {"step": "TOOL", "tool" : "get_weather", "input": "Delhi"}
OBSERVE: {"step": "OBSERVE", "tool" : "get_weather", "output": "The temperature of delhi is cloudy with 20 degree celsius"}
PLAN: {"step": "PLAN", "content": "Great, I got the weather info about delhi"}
OUTPUT: {"step": "OUTPUT", "content": "The current weather in delhi is 20 degree celsius with cloudy sky"}

"""

class MyOutputFormat(BaseModel):
   step: str = Field(...,description="The ID of the step. Example PLAN, OUTPUT, TOOL, etc")
   content: Optional[str] = Field(None, description="The optional string content for the step")
   tool: Optional[str] = Field(None, description="The ID of the tool to call")
   input: Optional[str] = Field(None, description="The input param for the tool to call")

message_history = [
    {"role" : "system", "content": SYSTEM_PROMPT}
]

available_tools = {
    "get_weather": get_weather
}

while True:
    user_query = input("👉🏻 ")
    message_history.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.parse(
          model="gemini-2.5-flash",
          response_format=MyOutputFormat,
          messages=message_history
        )

        raw_result = response.choices[0].message.content
        message_history.append({"role":"assistant", "content":raw_result})

        parse_result = response.choices[0].message.parsed

        if(parse_result.step == "START"):
          print("🔥", parse_result.content)
          continue

        if(parse_result.step == "TOOL"):
           tool_to_call = parse_result.tool
           tool_input = parse_result.input
           tool_response = available_tools[tool_to_call](tool_input)
   
           message_history.append({"role":"developer", "content":json.dumps(
               {"step":"OBSERVE", "tool": tool_to_call, "input":tool_input, "output":tool_response}
           )})
           continue

        if(parse_result.step == "PLAN"):
          print("🧠", parse_result.content)
          continue

        if(parse_result.step == "OUTPUT"):
          print("🤖", parse_result.content)
          break





#cmd + shft + p -> to toggle word wrap, for wrapping the big sentence





