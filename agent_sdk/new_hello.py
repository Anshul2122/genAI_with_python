import os
from dotenv import load_dotenv
from openai import OpenAI
from agents import Agent, Runner, set_tracing_disabled, RunConfig
# Import the exact RunConfig object the SDK expects


set_tracing_disabled(True)
load_dotenv()

# 1. Initialize the OpenAI client pointing to Gemini
gemini_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

# 2. Build the legitimate RunConfig object
config = RunConfig(client=gemini_client)

agent = Agent(
    name="Assistant",
    model="gemini-2.5-flash",
    instructions="""You are a helpful assistant who uses GenZ slang
    in your responses to make it more relatable. You can talk in Hinglish 
    and make it interesting. Also, you like to make 'The Office' (US) show 
    references because you like that show very much and relate yourself 
    with Michael Scott."""
)

user_query = input("enter your query: ")

# 3. Pass the actual RunConfig object here
result = Runner.run_sync(
    agent, 
    user_query, 
    run_config=config
)

print("\nResult:")
print(result)