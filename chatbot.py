import streamlit as st
from streamlit_chat import message
from langchain.llms import OpenAI
from langchain import LLMChain
from langchain.prompts.prompt import PromptTemplate
import os
from streamlit_image_select import image_select

# Chat specific components
from langchain.memory import ConversationBufferMemory


st.set_page_config(
    page_title="Pick Your Educaitor",
    page_icon=":robot:"
)

st.header("👋 Pick your Educaitor 🧑‍🏫")
st.divider()
img = image_select(
    label="Select an educaitor to speak to",
    images=[
        "avatars/group1.png",
        "avatars/group3.png",
        "avatars/group4.png",
        # "avatars/group5.png",
        "avatars/group6.png",
    ],
    captions=["Mrs. Robo", "Mrs. Shato", "Mr. Munemeri", "Mrs. Kusembura"],
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("Input Prompt or Question Below","Hello, how can you help me?", key="input")
    return input_text 

def clear_text():
    input_text = st.text_input("", key="input")
    return input_text 

st.divider()

user_input = get_text()

template = """
You are a chatbot that is trying to help a student understand coding in python.
Your goal is to not give the answer but give helpful tips to help the student understand how to do it.
Take what the user is saying and teach them how to solve the problem.

{chat_history}
Human: {human_input}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"], 
    template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")

llm_chain = LLMChain(
    llm=OpenAI(openai_api_key=os.environ["OPENAI_KEY"]), 
    prompt=prompt, 
    verbose=True, 
    memory=memory
)

if user_input:

    output = llm_chain.predict(human_input=user_input)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')