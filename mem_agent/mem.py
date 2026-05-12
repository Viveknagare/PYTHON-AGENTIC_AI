from dotenv import load_dotenv
load_dotenv()

from mem0 import Memory
import os
import json
from openai import OpenAI

client = OpenAI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = {
    "version" : "v1.1",
    "embedder" : {
        "provider" : "openai",
        "config" : {"api_key" : OPENAI_API_KEY, "model" : "text-embedding-3-small"}
    },
    "llm" : {
        "provider" : "openai",
        "config" : {"api_key" : OPENAI_API_KEY, "model" : "gpt-4.1"}
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
        }
    }
}

mem_client = Memory.from_config(config)

while True:
  
  user_query = input("> ").strip()

  search_memory = mem_client.search(query=user_query, filters={"user_id": "vivek"})

  memories = [
    f"ID: {mem.get('id')}\nMemory:{mem.get('memory')}" for mem in search_memory.get("results", [])
  ]

  print("found memories", memories)

  SYSTEM_PROMPT = f"""
    You are a helpful AI assistant with access to long-term memory about the user.
    
    The following memories are facts previously learned about the user.
    Use them to answer questions about the user whenever relevant.
    
    If the answer is present in memory, respond confidently using that information.
    Do NOT say that you don't know the user's name if it is included in memory.
    
    User Memories:
    {json.dumps(memories, indent=2)}
    
    Answer the user's question using these memories whenever possible.
  """
  
  response = client.chat.completions.create(
      model="gpt-4.1-mini",
      messages=[
          {"role" : "system", "content" : SYSTEM_PROMPT},
          {"role" : "user", "content" : user_query}
      ]
  )
  
  ai_response = response.choices[0].message.content
  print("AI:",ai_response)
  
  mem_client.add(
      user_id="vivek",
      messages=[
          {"role" : "user", "content" : user_query},
          {"role" : "assistant", "content" : ai_response}
      ]
  )
  
  print("Memory has been saved")