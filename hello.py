# !pip install smolagents[litellm]
from smolagents import CodeAgent, LiteLLMModel
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = LiteLLMModel(model_id="openai/gpt-4o", api_key=OPENAI_API_KEY) # Could use 'gpt-4o'
agent = CodeAgent(tools=[], model=model, add_base_tools=True)

agent.run("Could you give me the 118th number in the Fibonacci sequence?")