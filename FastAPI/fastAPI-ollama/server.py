
from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()

client = Client(
    host="http://localhost:11434"
)
@app.post("/")
def chat(message:str = Body(..., description = "The message")):
    response = client.chat(model="gemma:2b", messages=[
        {"role":"user", "content": message}
    ])
    return {"response":response.message.content}
    

# @app.get("/")
# def read_root():
#     return "Hello vivek"

# @app.get("/contact")
# def contactdetails():
#     return {"email" : "vivekbnagare31@gmail.com"}