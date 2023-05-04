import streamlit as st
from streamlit_chat import message
from langchain.llms import OpenAI
from langchain import LLMChain
from langchain.prompts.prompt import PromptTemplate

# Chat specific components
from langchain.memory import ConversationBufferMemory

st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)


st.header("Educait Chat - Teaching Assistant")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ","Hello, how are you?", key="input")
    return input_text 


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
    llm=OpenAI(openai_api_key='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'), 
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