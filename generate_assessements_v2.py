import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os

instruction = "\nReturn the answers in the following format:\n1. Question\nA) Option A\nB) Option B\nC) Option C\nD) Option D\n\nReturn the correct answers at the end of the response, all as one lump response on a single line, in the following format:\nAnswers: A, B, C, D, C, A"
template = """Generate 5 Multiple-Choice quiz questions and their respective answers for the following content:\n
    {content}
    {instruction}

"""

prompt = PromptTemplate(
    input_variables=["content", "instruction"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    llm = OpenAI(temperature=.2, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Educait Tools", page_icon=":robot:")
st.header("Educait: Generate asssessments")


col1, col2 = st.columns(2)
with col1:
    option_num_questions = st.selectbox(
        'How many questions should we generate?',
        ('5', '10'))

with col2:
    option_difficulty_level = st.selectbox(
        'Which difficulty level would you like?',
        ('Easy', 'Medium', 'Hard'))
st.markdown("## Insert content")

openai_api_key = os.environ["OPENAI_KEY"]


def get_text():
    input_text = st.text_area(label="Content Input", label_visibility='collapsed', placeholder="I want to get assessment for...", key="content_input")
    return input_text

content_input = get_text()

if len(content_input.split(" ")) > 700:
    st.write("Please enter shorter content. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.content_input = "In cryptography, a cipher block chaining message authentication code (CBC-MAC) is a technique for constructing a message authentication code (MAC) from a block cipher. The message is encrypted with some block cipher algorithm in cipher block chaining (CBC) mode to create a chain of blocks such that each block depends on the proper encryption of the previous block. This interdependence ensures that a change to any of the plaintext bits will cause the final encrypted block to change in a way that cannot be predicted or counteracted without knowing the key to the block cipher."

st.button("*See An Example*", type='secondary', help="Click to see an example of content", on_click=update_text_with_example)

st.markdown("### Assessment:")

if content_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_content = prompt.format(content=content_input, instruction=instruction)

    assessment = llm(prompt_with_content)

    st.write(assessment)