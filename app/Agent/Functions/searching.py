from langchain_community.tools.tavily_search import TavilySearchResults

search = TavilySearchResults(name="internet_search", max_results=3)