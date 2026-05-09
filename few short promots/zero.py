from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = "You are a helpful assistant but only if query by user is not related to AI. If query is related to AI, you will respond with 'I am sorry, I cannot answer that question because it is related to AI.'"

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "can you tell me about pikachu?"}
    ]
)

print(response.choices[0].message.content)
# zero-short prompting : the model is given a direct question of task without prior examples.
# The model is expected to generate a response based on its understanding of the task from the question alone.