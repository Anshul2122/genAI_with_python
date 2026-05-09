from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """You are a helpful assistant but only if query by user is not related to AI. 
If query is related to AI, you will respond with 'I am sorry, I cannot answer that question because it is related to AI.'
Rule:
-Strictly follow the output should in different language from the input.

"""
# Here are some examples of how you should respond to user queries:
# User: can you tell me about pikachu?
# Assistant: Pikachu is a popular Pokémon character known for its yellow fur and electric abilities.
# User: can you tell me about machine learning?
# Assistant: I am sorry, I cannot answer that question because it is related to AI.

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "can you tell me about AI/ML?"}
    ]
)

print(response.choices[0].message.content)
#few-short prompting : the model is given a direct question of task along with few examples of input-output pairs.
# The model is expected to generate a response based on its understanding of the task from the question