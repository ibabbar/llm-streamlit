import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os

template = """
    Below are python concepts that I need to make multiple choice assessments targetted for high schoolers.
    Your goal is to:
    - Produce {num_questions} questions and multiple choice answers for different levels of difficulty
    - Provide an answer key

    Here are some examples different python topics:
    - Variables and Conditionals
    - Arrays and Lists
    - Loops and Iteration
    - Functions
    - File Input/Output
    - Object-Oriented Programming
    - Encapsulation and Constructors
    
    Below is the difficulty level, number of questions and topic:
    Difficulty level: {difficulty}
    Topic: {topic}

"""

prompt = PromptTemplate(
    input_variables=["difficulty", "num_questions", "topic"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Educait Tools", page_icon=":robot:")
st.header("Educait: Generate asssessments")

col1, col2 = st.columns(2)

st.markdown("## Enter the topic you want your assessment for")

openai_api_key = os.environ["OPENAI_KEY"]

col1, col2 = st.columns(2)
with col1:
    option_num_questions = st.selectbox(
        'How many questions should we generate?',
        ('5', '10'))

with col2:
    option_difficulty_level = st.selectbox(
        'Which difficulty level would you like?',
        ('Easy', 'Medium', 'Hard'))

def get_text():
    input_text = st.text_area(label="Topic Input", label_visibility='collapsed', placeholder="I want to get assessment for...", key="topic_input")
    return input_text

topic_input = get_text()

if len(topic_input.split(" ")) > 700:
    st.write("Please enter a shorter topic. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.topic_input = "Arrays and List"

st.button("*See An Example*", type='secondary', help="Click to see an example of a topic", on_click=update_text_with_example)

st.markdown("### Assessment:")

if topic_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_topic = prompt.format(topic=topic_input, difficulty=option_difficulty_level, num_questions=option_num_questions)

    assessment = llm(prompt_with_topic)

    st.write(assessment)