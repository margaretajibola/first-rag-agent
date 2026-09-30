# First RAG Agent

A conversational AI agent built with LangGraph and GPT-4o that combines Retrieval-Augmented Generation (RAG) with tool use to answer questions about gala guests.

## How it works

The agent uses a LangGraph state graph with two nodes — an assistant (GPT-4o) and a tools node — and routes between them based on whether a tool call is needed.

It has access to 3 tools:
- `guest_info_retriever` — BM25 retrieval over a guest dataset to look up gala invitees by name or relation
- `get_weather_info` — returns weather info for a given location
- `DuckDuckGoSearchRun` — web search for general queries

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Run

```bash
python app.py
```

## Requirements

- Python 3.9+
- OpenAI API key
