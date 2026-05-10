from dotenv import load_dotenv
load_dotenv()
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_openai  import ChatOpenAI
import os
os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
        model="gemini-2.5-flash",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )


class State(TypedDict):
    """State of the chat."""
    messages: Annotated[list, add_messages]
    


def chatbot(state:State):
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}


def end(state:State):
   response = llm.invoke(state.get("messages"))
   return {"messages": [response]}


def middle(state:State):
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("middle", middle)
graph_builder.add_node("end", end)

# (start) --> chatbot --> middle --> end --> (end)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "middle")
graph_builder.add_edge("middle", "end")
graph_builder.add_edge("end", END)


graph = graph_builder.compile()
updated_graph = graph.invoke({"messages": ["Hi! its none of your business"]})

print("\n\nUpdated graph:", updated_graph)