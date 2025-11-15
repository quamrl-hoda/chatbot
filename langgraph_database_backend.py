from langgraph.graph import StateGraph, START,END
from typing import TypedDict,Annotated,Literal
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import operator
from langchain_core.messages import HumanMessage, SystemMessage,BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3

load_dotenv()  # take environment variables from .env file

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


class ChatState(TypedDict):

  messages:Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState):
  messages = state['messages']
  response = llm.invoke(messages)
  return {'messages': [response]}

conn = sqlite3.connect(database='chatbot.db',check_same_thread=False )
# checkpointer to save state
checkpointer = SqliteSaver(conn = conn)


graph = StateGraph(ChatState)
graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)


chatbot = graph.compile(checkpointer=checkpointer)

# #
# CONFIG = {'configurable':{'thread_id':'thread-1'}}

# response = chatbot.invoke(
#             {'messages':[HumanMessage(content='What is the capital of india acknowledged my name and give me in detail why it is?')]},
#             config=CONFIG
# )
# print(response)
def retrieve_all_threads():
  all_threads = set()
  for checkpoint in chatbot.checkpointer.list(None):
      all_threads.add(checkpoint.config['configurable']['thread_id'])
  return list(all_threads)
