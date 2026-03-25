"""
backend/graph_tools.py
Tool-augmented LangGraph chatbot (search + calculator + stock price).
Uses SQLite persistence and Gemini as the reasoning model.
"""
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from dotenv import load_dotenv

from typing import TypedDict, Annotated
import sqlite3
import requests
import os

load_dotenv()

# ── Database ──────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "chatbot.db")
conn = sqlite3.connect(database=DB_PATH, check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

# ── LLM ───────────────────────────────────────────────────────────────────────
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)

# ── Tools ─────────────────────────────────────────────────────────────────────
search_tool = DuckDuckGoSearchRun()


@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """Basic arithmetic calculator tool."""
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "ZeroDivisionError"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        return {"first_num": first_num, "second_num": second_num,
                "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}


@tool
def get_stock_price(symbol: str) -> dict:
    """Fetch stock price using Alpha Vantage."""
    API_KEY = "QJWPWEPINLFR1A15"
    url = (
        f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE"
        f"&symbol={symbol}&apikey={API_KEY}"
    )
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


tools = [search_tool, calculator, get_stock_price]
llm_with_tools = llm.bind_tools(tools)

# ── State ─────────────────────────────────────────────────────────────────────
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ── Nodes ─────────────────────────────────────────────────────────────────────
def chat_node(state: ChatState):
    """LLM reasoning / tool-calling node."""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


tool_node = ToolNode(tools)

# ── Graph ─────────────────────────────────────────────────────────────────────
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

chatbot = graph.compile(checkpointer=checkpointer)


# ── Helpers ───────────────────────────────────────────────────────────────────
def retrieve_all_threads() -> list[str]:
    """Return unique thread_ids from saved checkpoints."""
    try:
        checkpoints = checkpointer.list(None)
    except TypeError:
        return []

    threads: set[str] = set()
    for c in checkpoints:
        try:
            cfg = c.get("config", {}) if isinstance(c, dict) else getattr(c, "config", {}) or {}
            if isinstance(cfg, dict):
                thread_id = cfg.get("configurable", {}).get("thread_id")
            else:
                configurable = getattr(cfg, "configurable", None)
                thread_id = getattr(configurable, "thread_id", None) if configurable else None
            if thread_id:
                threads.add(thread_id)
        except Exception:
            continue
    return list(threads)
