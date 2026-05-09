from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        
        {"role": "system", "content": "You are a helpful assistant but only if query by user is not related to AI. If query is related to AI, you will respond with 'I am sorry, I cannot answer that question because it is related to AI.'"},
        # role - system is used to set the behavior of the assistant. In this case, we are instructing the assistant to be helpful but to avoid answering questions related to AI.
        {"role": "user", "content": "Explain AI simply"}
    ]
)

print(response.choices[0].message.content)
