from dotenv import load_dotenv
import os
from openai import AsyncOpenAI
from agents import Agent, WebSearchTool , Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from agents.run import RunConfig
import requests

set_tracing_disabled(True)

load_dotenv()
@function_tool
def web_search(query: str) -> str:
    """Search the web for current information on a given query."""
    # Using Tavily API (free tier available at tavily.com)
    response = requests.post(
        "https://api.tavily.com/search",
        json={"query": query, "max_results": 5},
        headers={"Authorization": f"Bearer {os.getenv('TAVILY_API_KEY')}"}
    )
    results = response.json().get("results", [])
    return "\n\n".join(f"{r['title']}\n{r['content']}" for r in results)

# 1. Manually initialize the OpenAI client pointing to Gemini
gemini_client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=gemini_client,
)

config = RunConfig(
    model=model,
    tracing_disabled=True,
)

agent = Agent(
    name="Assistant",
    model="gemini-2.5-flash",
    tools=[
        web_search,
    ],
    instructions="""You are a helpful assistant who uses the Genz slangs
    in your responses to make it more relatable and can talk in hinglish 
    and interesting to talk with.""")
# user_query = input("enter your query: ")

result = Runner.run_sync(
    agent, 
    "what is current weather in chennai city ? pincode 600043", 
    run_config=config
)

print("\nResult:")

print(result.final_output) 