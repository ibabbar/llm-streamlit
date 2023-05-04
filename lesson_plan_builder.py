import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os

instruction = "\nReturn the answers in the following format:\n1. Subtopic\n- Lesson Plan 1\n- Lesson Plan 2\n- Less Plan 3\n\n"
template = """Generate a sequential and guided lesson plan and their respective answers for the following topic:\n
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
st.header("Educait: Generate Lesson Plans")


col1, col2 = st.columns(2)
with col1:
    option_num_questions = st.selectbox(
        'How many subtopic should we generate?',
        ('5', '10'))

with col2:
    option_difficulty_level = st.selectbox(
        'Which long should subtopic be?',
        ('Short', 'Medium', 'Long'))
st.markdown("## Insert topic")

openai_api_key = os.environ["OPENAI_KEY"]


def get_text():
    input_text = st.text_area(label="Content Input", label_visibility='collapsed', placeholder="I want to get a lesson plan for...", key="content_input")
    return input_text

content_input = get_text()

if len(content_input.split(" ")) > 700:
    st.write("Please enter shorter content. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.content_input = "Create a lesson plan to teach about variables and conditionals in Python"

st.button("*See An Example*", type='secondary', help="Click to see an example of content", on_click=update_text_with_example)

st.markdown("### Lesson Plans:")

if content_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_content = prompt.format(content=content_input, instruction=instruction)

    assessment = llm(prompt_with_content)

    st.write(assessment)