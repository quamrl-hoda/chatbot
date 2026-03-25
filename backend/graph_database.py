"""
backend/graph_database.py
SQLite-persisted LangGraph chatbot — conversations survive server restarts.
"""
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, BaseMessage
from dotenv import load_dotenv

from typing import TypedDict, Annotated
import sqlite3
import os

load_dotenv()

# ── Database ──────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "chatbot.db")
conn = sqlite3.connect(database=DB_PATH, check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

# ── LLM ───────────────────────────────────────────────────────────────────────
llm = ChatOpenAI(model="gpt-4o-mini")


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# ── Graph ─────────────────────────────────────────────────────────────────────
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)


# ── Helpers ───────────────────────────────────────────────────────────────────
def retrieve_all_threads() -> list[str]:
    """Return all unique thread_ids stored in the SQLite checkpoint."""
    all_threads: set[str] = set()
    for checkpoint in chatbot.checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)
