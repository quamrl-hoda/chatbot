# Project Structure

```
chatbot/
├── backend/                        ← LangGraph graph definitions
│   ├── __init__.py
│   ├── graph_memory.py             ← In-memory chatbot  (was: langgraph_backend.py)
│   ├── graph_database.py           ← SQLite chatbot     (was: langgraph_database_backend.py)
│   └── graph_tools.py              ← Tool-augmented bot (was: langgraph_tool_backend.py)
│
├── frontend/                       ← Streamlit UIs
│   ├── __init__.py
│   ├── streaming.py                ← Basic streaming    (was: streamlit_frontend_streaming.py)
│   ├── threading.py                ← Multi-thread       (was: streamlit_frontend_threading.py)
│   ├── database.py                 ← DB-persisted       (was: streamlit_frontend_database.py)
│   └── tools.py                    ← Tool chatbot UI    (was: streamlit_tool_frontend.py)
│
├── data/
│   └── chatbot.db                  ← SQLite database (moved from root)
│
├── .env                            ← API keys
├── .gitignore
├── .python-version
├── requirements.txt
├── pyproject.toml
└── README.md
```

## How to Run

```bash
# SQLite-persisted chatbot (recommended — survives restarts)
streamlit run frontend/database.py

# Tool-augmented chatbot (search + calculator + stock)
streamlit run frontend/tools.py

# In-memory multi-thread chatbot
streamlit run frontend/threading.py

# Basic single-thread streaming
streamlit run frontend/streaming.py
```

> [!IMPORTANT]
> All commands must be run from the **`chatbot/`** root directory so that Python resolves `backend.*` imports correctly.

## What Changed

| Old file | New location | Notes |
|---|---|---|
| [langgraph_backend.py](file:///c:/Users/quamr/OneDrive/Desktop/project/langchainLLM/chatbot/langgraph_backend.py) | [backend/graph_memory.py](file:///c:/Users/quamr/OneDrive/Desktop/project/langchainLLM/chatbot/backend/graph_memory.py) | |
| [langgraph_database_backend.py](file:///c:/Users/quamr/OneDrive/Desktop/project/langchainLLM/chatbot/langgraph_database_backend.py) | [backend/graph_database.py](file:///c:/Users/quamr/OneDrive/Desktop/project/langchainLLM/chatbot/backend/graph_database.py) | DB path now relative to file |
| [langgraph_tool_backend.py](file:///c:/Users/quamr/OneDrive/Desktop/project/langchainLLM/chatbot/langgraph_tool_backend.py) | [backend/graph_tools.py](file:///c:/Users/quamr/OneDrive/Desktop/project/langchainLLM/chatbot/backend/graph_tools.py) | DB path now relative to file |
| [streamlit_frontend_streaming.py](file:///c:/Users/quamr/OneDrive/Desktop/project/langchainLLM/chatbot/streamlit_frontend_streaming.py) | [frontend/streaming.py](file:///c:/Users/quamr/OneDrive/Desktop/project/langchainLLM/chatbot/frontend/streaming.py) | |
| [streamlit_frontend_threading.py](file:///c:/Users/quamr/OneDrive/Desktop/project/langchainLLM/chatbot/streamlit_frontend_threading.py) | [frontend/threading.py](file:///c:/Users/quamr/OneDrive/Desktop/project/langchainLLM/chatbot/frontend/threading.py) | |
| [streamlit_frontend_database.py](file:///c:/Users/quamr/OneDrive/Desktop/project/langchainLLM/chatbot/streamlit_frontend_database.py) | [frontend/database.py](file:///c:/Users/quamr/OneDrive/Desktop/project/langchainLLM/chatbot/frontend/database.py) | |
| [streamlit_tool_frontend.py](file:///c:/Users/quamr/OneDrive/Desktop/project/langchainLLM/chatbot/streamlit_tool_frontend.py) | [frontend/tools.py](file:///c:/Users/quamr/OneDrive/Desktop/project/langchainLLM/chatbot/frontend/tools.py) | Now has ChatGPT-style labels too |
| [chatbot.db](file:///c:/Users/quamr/OneDrive/Desktop/project/langchainLLM/chatbot/chatbot.db) | `data/chatbot.db` | |
