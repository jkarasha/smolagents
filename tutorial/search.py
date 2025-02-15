# This code creates a tool that runs DuckDuckGo searches. It uses the smolagents package,
# which provides a way to create "tools" that can be used by agents. The DuckDuckGoSearchTool
# tool takes a query as input and returns the search results as output.
from smolagents import DuckDuckGoSearchTool

search_tool = DuckDuckGoSearchTool()

print(search_tool("Who's the current president of Russia?"))