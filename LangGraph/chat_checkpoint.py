from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver  

load_dotenv()

llm = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai"
)

# define state
class State(TypedDict):
    messages : Annotated[list, add_messages]

# write nodes - they are nothing but functions that update the state
def chatbot(state : State):
    response = llm.invoke(state.get("messages"))
    # they update and return the state
    return {"messages" : [response]}


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# (START) -> chatbot -> samplenode -> (END)
graph = graph_builder.compile()

def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

    
DB_URI="mongodb://admin:admin@localhost:27017"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
  graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer=checkpointer)
  
  config = {
      "configurable" : {
          "thread_id" : "vivek"
      }
  }
  
  for chunk in graph_with_checkpointer.stream(
      State({"messages":["what is my name"]}),
      config,
      stream_mode="values"
      ):
      chunk["messages"][-1].pretty_print()
  
  # in my checkpointer message = hey my name is vivek will be stored under id = vivek
  
