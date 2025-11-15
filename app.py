import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage,BaseMessage

CONFIG = {'configurable':{'thread_id':'thread-1'}}
# st.session+state -> dictionary to hold message history
if 'messages_history' not in st.session_state:
    st.session_state['messages_history'] = []
# loading message history
for message in st.session_state['messages_history']:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Type here...")

if user_input:
  # first add the message to message history
  st.session_state['messages_history'].append({"role":"user","content":user_input})
  with st.chat_message("user"):
      st.text(user_input)

  response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]}, config=CONFIG)
  ai_message = response['messages'][-1].content
  #first add the message to message history
  st.session_state['messages_history'].append({"role":"assistant","content":ai_message})
  with st.chat_message("assistant"):
     st.text(ai_message)