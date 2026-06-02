# from dotenv import load_dotenv
# load_dotenv()
# import os
# from mem0 import Memory
# from openai import OpenAI



# client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"),
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# MEM0_API_KEY = os.getenv("MEM0_API_KEY")


# config ={
#     "version":"v1.1",
#     "embedder": {
#     "provider": "gemini",
#     "config": {
#         "api_key": GEMINI_API_KEY,
#         "model": "models/gemini-embedding-001"  # no "models/" prefix
#         }        
#     },
#     "llm":{
#          "provider": "gemini",
#         "config": {
#             "api_key": GEMINI_API_KEY,
#             "model": "gemini-2.5-flash"
#         }
#         },
#     "vector_store":{
#         "provider":"qdrant",
#         "config":{
#             "host":"localhost",
#             "port":6333,
#         }
#     }
# }

# mem_client = Memory.from_config(config)


# user_query = input("What would you like to ask? ")

# response = client.chat.completions.create(
#     model="gemini-2.5-flash",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": user_query}
#     ]
# )

# ai_res = response.choices[0].message.content


# print("Response from LLM:")
# print(ai_res)

# mem_client.add(
#     user_id="user_123",
#     messages=[
#         {"role":"user", "content": user_query},
#         {"role":"assistant", "content": ai_res}
#     ]
# )

# print("Conversation added to memory.")

from dotenv import load_dotenv
load_dotenv()
import os
from mem0 import Memory
from openai import OpenAI
import json

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MEM0_API_KEY = os.getenv("MEM0_API_KEY")
NEO_USERNAME= os.getenv("NEO_USERNAME")
NEO_PASSWORD= os.getenv("NEO_PASSWORD")
NEO_CONNECT_URI= os.getenv("NEO_CONNECT_URI")

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "gemini",
        "config": {
            "api_key": GEMINI_API_KEY,
            "model": "models/gemini-embedding-001"
        }
    },
    "llm": {
        "provider": "gemini",
        "config": {
            "api_key": GEMINI_API_KEY,
            "model": "gemini-2.5-flash"
        }
    },
    "graph_store": { 
        "provider": "neo4j",
        "config": {
            "username": NEO_USERNAME,
            "password": NEO_PASSWORD,
            "connect_uri": NEO_CONNECT_URI
        },
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

while(True):

    user_query = input("What would you like to ask? ")

    search_memory = mem_client.search(query=user_query, user_id="user_123")
    
    memory_about_user = [
        f"ID: {mem.get('id')}, Content: {mem.get('memory')}"
        for mem in search_memory.get("results")
    ]
    
    print("found memoeries", memory_about_user)
    
    SYSTEM_PROMPT = f"""
        here is the context about the user:
        {json.dumps(memory_about_user)}
    """

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )

    ai_res = response.choices[0].message.content
    print("Response from LLM:")
    print(ai_res)



    mem_client.add(
        user_id="user_123",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_res}
        ]
    )

    print("Conversation added to memory.")