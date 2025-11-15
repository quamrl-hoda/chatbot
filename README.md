
# 🤖 **Modular AI Chatbot — LangChain + LangGraph**

A fully modular, intelligent AI chatbot built using **LangChain** and **LangGraph**, designed for dynamic conversations, memory management, and graph-based reasoning.
This project demonstrates how to build a production-ready conversational agent using modern LLM frameworks, structured workflows, and flexible tool integration.

---

##  **Features**

*  **LangChain-powered architecture**
*  **LangGraph workflow engine** for flexible control flow
*  **Conversation memory** (short-term + long-term ready)
*  **RAG-ready design** (optional)
*  **Tool execution support**
*  **Deterministic conversational routing** using Graph nodes
*  Optional **FastAPI backend**
*  Clean, extensible code structure

---

## **Project Structure**

```
chatbot/
├── src/
│   ├── agents/
│   │   └── chatbot_agent.py
│   ├── graph/
│   │   └── chatbot_graph.py
│   ├── chains/
│   ├── memory/
│   │   └── memory_manager.py
│   ├── api/
│   │   └── main.py        # (optional FastAPI server)
│   └── utils/
├── .env
├── requirements.txt
└── README.md
```

---


### **1. Clone the Repository**

```bash
git clone https://github.com/yourusername/chatbot-langchain-langgraph.git
cd chatbot-langchain-langgraph
```

### **2. Create a Virtual Environment**

```bash
python -m venv myenv
myenv\Scripts\activate     # Windows
source myenv/bin/activate  # macOS/Linux
```

### **3. Install Requirements**

```bash
pip install -r requirements.txt
```

### **4. Add Your API Keys (.env file)**

Example:

```
OPENAI_API_KEY=your_key_here
```

Then load using:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

##  **How It Works**

### ** LangChain Base**

Handles:

* LLM calls
* Conversation chains
* Tool usage
* Prompts

### ** LangGraph Workflow**

Manages:

* Conditional routing
* Stateful graph nodes
* Multi-step agent reasoning
* Error handling paths

### ** Memory Layer**

Supports:

* Conversation history
* Context persistence
* Extensible memory modules

### ** Optional RAG Integration**

You can plug in:

* Vector databases (FAISS / Chroma)
* PDF ingestion
* Knowledge retrieval pipelines

---

##  **Optional API Server (FastAPI)**

Run:

```bash
uvicorn src.api.main:app --reload
```

Swagger UI:
 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## **Example Usage**

```python
from src.agents.chatbot_agent import create_chatbot

bot = create_chatbot()

response = bot.invoke({"input": "Hello, how are you?"})
print(response)
```

---

## **Testing**

If you have tests set up:

```bash
pytest tests/
```

---

##  **Roadmap**

* [ ] Add RAG pipeline
* [ ] Add multi-agent workflow
* [ ] Add Streamlit frontend
* [ ] Add conversation visualization
* [ ] Add tool execution examples
* [ ] Add memory persistence (SQLite / Redis)

---

##  **Contributing**

1. Fork the repo
2. Create a feature branch
3. Commit improvements
4. Open a pull request

PRs are welcome!

---

##  **License**

MIT License — free for personal and commercial projects.

---

