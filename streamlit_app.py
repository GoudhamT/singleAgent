
import os
import sys
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

# --------------------------------------------------
# 1. Project configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()

from backend.config.settings import settings

from langchain.tools import tool
from langchain.agents import create_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI


# --------------------------------------------------
# 2. Streamlit page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Assistant")
st.caption("Powered by LangChain, OpenRouter, Tavily and WeatherStack")


# --------------------------------------------------
# 3. WeatherStack Tool
# --------------------------------------------------

@tool
def get_current_weather(location: str) -> dict:
    """
    Fetch current weather details for a given city or location.
    Returns only current weather information.
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

        return data.get("current", {})

    except requests.exceptions.Timeout:
        return {"error": "WeatherStack API request timed out."}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    except ValueError:
        return {"error": "Invalid JSON response from WeatherStack."}


# --------------------------------------------------
# 4. Initialize LangChain Agent
# --------------------------------------------------

@st.cache_resource
def get_agent():

    # Tavily reads its API key from the environment
    os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY

    search_tool = TavilySearchResults(
        max_results=3
    )

    model = ChatOpenAI(
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        max_tokens=2000
    )

    agent = create_agent(
        model=model,
        tools=[
            search_tool,
            get_current_weather
        ],
        system_prompt="""
        You are a helpful AI assistant.

        Instructions:
        1. Answer general questions using your knowledge.
        2. Use Tavily search for current information and web research.
        3. Use get_current_weather for current weather queries.
        4. Never invent search results or weather information.
        5. Provide clear and concise answers.
        """
    )

    return agent


# --------------------------------------------------
# 5. Initialize Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# 6. Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    st.write("**Available Tools**")

    st.success("🌐 Tavily Web Search")
    st.success("🌤️ WeatherStack API")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------
# 7. Display Chat History
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# 8. User Input and Agent Execution
# --------------------------------------------------

if prompt := st.chat_input("Ask me anything..."):

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Execute LangChain agent
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                agent = get_agent()

                result = agent.invoke({
                    "messages": st.session_state.messages
                })

                answer = result["messages"][-1].content

                st.markdown(answer)

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                error_message = f"Something went wrong: {str(e)}"

                st.error(error_message)
