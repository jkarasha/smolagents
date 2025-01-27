import os
from smolagents import CodeAgent, AzureOpenAIServerModel
from dotenv import load_dotenv


load_dotenv()

model = AzureOpenAIServerModel(
    model_id = "gpt-4o-mini",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION")    
)

agent = CodeAgent(tools=[], model=model, add_base_tools=True)

agent.run("Could you give me the 118th number in the Fibonacci sequence?")