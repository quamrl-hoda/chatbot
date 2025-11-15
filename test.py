import streamlit as st


with st.chat_message("user"):
    st.text("Hello!")


with st.chat_message("assistant"):
    st.text("Hi there! How can I assist you today?")


with st.chat_message("assistant"):
    st.text("What would you like to know about LangGraph?")



user_input= st.chat_input("Type here...")


if user_input:
    with st.chat_message("user"):
        st.text(user_input)
    
    with st.chat_message("assistant"):
        st.text("I'm here to help! What specific information are you looking for regarding LangGraph?")