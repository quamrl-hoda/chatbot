"""
frontend/tools.py
Tool-augmented multi-thread chatbot (search, calculator, stock price).
Run: streamlit run frontend/tools.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from backend.graph_tools import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid


# ── Utilities ─────────────────────────────────────────────────────────────────
def generate_thread_id():
    return uuid.uuid4()


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def load_conversation(thread_id) -> list:
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    return state.values.get("messages", [])


def get_thread_label(thread_id) -> str:
    """Return the first user message as the sidebar label (max 40 chars)."""
    try:
        messages = chatbot.get_state(
            config={"configurable": {"thread_id": thread_id}}
        ).values.get("messages", [])
        for msg in messages:
            if isinstance(msg, HumanMessage):
                text = msg.content.strip()
                return text[:40] + ("…" if len(text) > 40 else "")
    except Exception:
        pass
    return str(thread_id)


# ── Session Setup ─────────────────────────────────────────────────────────────
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

add_thread(st.session_state["thread_id"])


# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Chats")

for thread_id in st.session_state["chat_threads"][::-1]:
    label = get_thread_label(thread_id)
    if st.sidebar.button(label, key=str(thread_id)):
        st.session_state["thread_id"] = thread_id
        messages = load_conversation(thread_id)
        temp = []
        for msg in messages:
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            temp.append({"role": role, "content": msg.content})
        st.session_state["message_history"] = temp


# ── Main UI ───────────────────────────────────────────────────────────────────
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Type here")

if user_input:
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
        "run_name": "chat_turn",
    }

    with st.chat_message("assistant"):
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})
