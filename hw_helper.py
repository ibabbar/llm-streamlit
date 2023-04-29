import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os

template = """
    Below are python concepts that I need to understand better.
    Your goal is to:
    - Answer the question with guiding explanations
    - Use specified tone
    - Use specified dialect
    - Make the text easy to read by avoid large paragraphs

    Here are some examples different python topics:
    - Variables and Conditionals
    - Arrays and Lists
    - Loops and Iteration
    - Functions
    - File Input/Output
    - Object-Oriented Programming
    - Encapsulation and Constructors


    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

    Please start the prompt with a warm introduction. Add the introduction if you need to.
    
    Below is the prompt, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    Prompt: {email}
    
    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "email"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Educait Tools", page_icon=":robot:")
st.header("Educait: Answer my questions about hw")

col1, col2 = st.columns(2)

# with col1:
#     st.markdown("")

# with col2:
#     st.image(image='TweetScreenshot.png', width=500, caption='https://twitter.com/DannyRichman/status/1598254671591723008')

st.markdown("## Enter what you want your questions are")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = os.environ["OPENAI_KEY"]#get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which topic do you want to talk about?',
        ('Variables and Conditionals', 'Arrays and Lists', 'Loops and Iteration', 'Functions', 'File Input/Output', 'Object-Oriented Programming', 'Encapsulation and Constructors'))

with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British', 'Zimbabwean'))

def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Answer this question...", key="email_input")
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 700:
    st.write("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "What are kwargs and args?"

st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Answers:")

if email_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, email=email_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)