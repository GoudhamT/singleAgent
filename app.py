import os
import sys
import certifi
import requests
from pathlib import Path
PROJECT_ROOT = Path.cwd().parent
sys.path.insert(0, str(PROJECT_ROOT))
from backend.config.settings import settings
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openrouter import ChatOpenRouter
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from rich import print as pt
import requests


# os.environ['SSL_CERT_FILE'] = certifi.where()

search_tool = TavilySearchResults(max_results=3,TAVILY_API_KEY=settings.TAVILY_API_KEY)

@tool
def get_current_weather(location: str) -> dict:
    """
    Fetch current weather details for a given city or location.
    Returns only the current weather data.
    """

    api_key = settings.WEATHERSTACK_API_KEY

    if not api_key:
        return {"error": "WeatherStack API key is not configured."}

    url = "https://api.apilayer.net/weatherstack/current"

    params = {
        "access_key": api_key,
        "query": location
    }

    headers = {
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if "error" in data:
            return {"error": data["error"]}

        # Return only current weather details
        return data.get("current", {})

    except requests.exceptions.Timeout:
        return {"error": "WeatherStack API request timed out."}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    except ValueError:
        return {"error": "Invalid JSON response from WeatherStack."}
    
model = ChatOpenAI(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    max_tokens = 2000
)

response = model.invoke("Say hello")
print(response.content,end='\n')

agent = create_agent(model=model, tools=[search_tool,get_current_weather])

result = agent.invoke({"messages": [{"role": "user", "content": "Summarize AI trends in 3 lines"}]})
print(result['messages'][-1].content,end='\n')

result = agent.invoke({"messages": [{"role": "user", "content": "what happened in 2026 senate US election, give me 20 words,today is 17th nov 2026 "}]})
print(result['messages'][-1].content,end='\n')

result = agent.invoke({"messages": [{"role": "user", "content": "what is capital of Canada and weather now? "}]})
print(result['messages'][-1].content,end='\n')

