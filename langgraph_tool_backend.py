from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# ❗ REMOVE SqliteSaver – DO NOT USE sqlite checkpointing
from langgraph.checkpoint.sqlite import SqliteSaver  
import sqlite3


from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

import requests

load_dotenv()

# ---- LLM ----
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)

# ---- Tools ----
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

        return {
            "first_num": first_num,
            "second_num": second_num,
            "operation": operation,
            "result": result
        }
    except Exception as e:
        return {"error": str(e)}

@tool
def get_stock_price(symbol: str) -> dict:
    """Fetch stock price using Alpha Vantage."""
    API_KEY = "QJWPWEPINLFR1A15"
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
    
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# Tool list
tools = [search_tool, calculator, get_stock_price]

# Make LLM tool-aware
llm_with_tools = llm.bind_tools(tools)

# ---- STATE ----
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# ---- NODES ----
def chat_node(state: ChatState):
    """LLM reasoning/tool-calling node."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

# ---- CHECKPOINTER (FIXED HERE) ----
# ❌ REMOVE SqliteSaver database checkpointing
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

# ---- GRAPH ----
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

# Compile final chatbot
chatbot = graph.compile(checkpointer=checkpointer)


# ---- THREAD RETRIEVAL ----
def retrieve_all_threads():
    """Return unique thread_ids from saved checkpoints (handles dict/object shapes)."""
    try:
        checkpoints = checkpointer.list()
    except TypeError:
        try:
            checkpoints = checkpointer.list(None)
        except Exception:
            return []

    threads = set()
    for c in checkpoints:
        try:
            # support dict-like checkpoint
            if isinstance(c, dict):
                cfg = c.get("config") or {}
            else:
                cfg = getattr(c, "config", None) or {}

            # cfg may be dict-like or object-like
            if isinstance(cfg, dict):
                thread_id = cfg.get("configurable", {}).get("thread_id")
            else:
                configurable = getattr(cfg, "configurable", None)
                thread_id = getattr(configurable, "thread_id", None) if configurable is not None else None

            if thread_id:
                threads.add(thread_id)
        except Exception:
            continue

    return list(threads)
