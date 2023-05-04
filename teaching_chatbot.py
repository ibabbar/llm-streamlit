import streamlit as st
from streamlit_chat import message
from langchain.llms import OpenAI
from langchain import LLMChain
from langchain.prompts.prompt import PromptTemplate
import os

# Chat specific components
from langchain.memory import ConversationBufferMemory

st.set_page_config(
    page_title="Educait Chat - Teacher's Assistant",
    page_icon=":robot:"
)


st.header("Educait Chat - Teacher's Assistant")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ","", key="input")
    return input_text 


user_input = get_text()

template = """
You are a chatbot that is trying to help a teacher to manage students, assignments, lesson plans, assessments.
Your goal give helpful explanations to help the teacher understand their classroom better.
Take what the teacher is saying and pretend to solve the problem.

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