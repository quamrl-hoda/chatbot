from langgraph.graph import StateGraph, START,END
from typing import TypedDict,Annotated,Literal
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import operator
from langchain_core.messages import HumanMessage, SystemMessage,BaseMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

load_dotenv()  # take environment variables from .env file

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


class ChatState(TypedDict):

  messages:Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState):
  messages = state['messages']
  response = llm.invoke(messages)
  return {'messages': [response]}


# checkpointer to save state
checkpointer = InMemorySaver()


graph = StateGraph(ChatState)
graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)


chatbot = graph.compile(checkpointer=checkpointer)


# for message_chunk,metadata in chatbot.stream(
#   {'messages':[HumanMessage(content='What is the recipe to make pasta')]},
#   config = {'configurable':{'thread_id':'thread-1'}},
#   stream_mode = 'messages'

# ): 
#   if message_chunk:
#     print(message_chunk.content, end=' ', flush=True)

# CONFIG = {'configurable':{'thread_id':'thread-1'}}

# respone = chatbot.stream(
#             {'messages':[HumanMessage(content='hi my name is quamrul')]},
#             config=CONFIG
#  )

# print(chatbot.get_state(config=CONFIG))