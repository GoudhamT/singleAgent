# AI Assistant 🤖

A simple AI-powered assistant built using **Python, LangChain, and Streamlit**. It can answer general questions, search the web, and provide current weather information using external APIs.

## Features

- Answer general questions using an LLM.
- Search the web using Tavily.
- Get current weather information using WeatherStack.
- Automatically select tools based on user questions.
- Maintain chat history during the active session.

## Technologies Used

- Python
- LangChain
- OpenRouter (LLM)
- Tavily Search API
- WeatherStack API
- Streamlit

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/GoudhamT/singleAgent.git
cd singleAgent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows:**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key
TAVILY_API_KEY=your_api_key
WEATHERSTACK_API_KEY=your_api_key
```

### 5. Run the application

```bash
streamlit run streamlit_app.py
```

Open your browser:

http://localhost:8501

## Author

Goudham T

GitHub: https://github.com/GoudhamT