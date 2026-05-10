from dotenv import load_dotenv
load_dotenv()

from typing_extensions import TypedDict
from typing import Annotated, Literal
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_openai  import ChatOpenAI
import os
from openai import OpenAI

from typing import Optional


os.getenv("OPENAI_API_KEY")

gemini_client = OpenAI(

    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# llm = ChatOpenAI(
#         model="gemini-2.5-flash",
#         base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#     )

class State(TypedDict):
    """State of the chat."""
    user_query:str
    llm_output: Optional[str]
    is_good = Optional[bool]


def chatbot(state:State):
    print("working with google gemini llm")
    response = gemini_client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": """You are a helpful assistant that answers the user's query. 
            If you don't know the answer, say you don't know. Be concise and to the point."""},
            {"role": "user", "content": state.get("user_query")}
        ]
    )
    state["llm_output"] = response.choices[0].message.content
    return state


def chatBot_groq(state: State):
    print
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Be concise and to the point."},
            {"role": "user", "content": state.get("user_query")}
        ]
    )
    state["llm_output"] = response.choices[0].message.content
    return state
    

def evaluate(state: State) -> Literal["chatBot_groq", "end"]:
    print("evaluating the answer with groq llm from eval function")
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Reply only 'yes' if this is a good answer, else reply 'no'. Nothing else."},
            {"role": "user", "content": f"Query: {state.get('user_query')}\nAnswer: {state.get('llm_output')}"}
        ]
    )
    verdict = response.choices[0].message.content.strip().lower()
    return "end" if verdict == "yes" else "chatBot_groq"
    


def end(state:State):
    print(f"\n✅ Final Answer: {state.get('llm_output')}")
    return state

graph_builder = StateGraph(State)
graph_builder.add_node("chatBot_groq", chatBot_groq)  # ← was missing
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("end", end)

graph_builder.add_edge(START, "chatBot_groq")
graph_builder.add_conditional_edges("chatbot", evaluate)
graph_builder.add_edge("chatbot", END)
graph_builder.add_edge("end", END)



# graph_builder.add_edge(START, "chatbot")
# graph_builder.add_conditional_edges("chatbot", evaluate)
# graph_builder.add_edge("chatBot_groq", END)
# graph_builder.add_edge("end", END)

    
graph = graph_builder.compile()

user_query = input("Enter your query: ")
result = graph.invoke({"user_query": user_query, "llm_output": None, "is_good": None})
print("\nFinal state:", result)