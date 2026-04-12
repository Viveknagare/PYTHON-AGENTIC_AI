from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# define state
class State(TypedDict):
    messages : Annotated[list, add_messages]

# write nodes - they are nothing but functions that update the state
def chatbot(state : State):
    print("\n\nInside chatbot node",state)
    # they update and return the state
    return {"messages" : ["Hey this is the message from chatbot"]}

def samplenode(state : State):
    print("\n\nInside samplenode", state)
    return {"messages" : ["Sample message appended"]}


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

# (START) -> chatbot -> samplenode -> (END)
graph = graph_builder.compile()
Updated_state = graph.invoke(State({"messages":["Hi My name is Vivek Nagare"]}))

print("\n\nUpdated state", Updated_state)