import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os 
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

template = """
    Write in a {tone} response that tells me the following healthcare benefits information: {response_input}

"""

prompt = PromptTemplate(
    input_variables=["tone", "response_input"],
    template=template,
)

def load_LLM(openai_api_key):
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="NayyaGPT", page_icon=":robot:")
st.header("NayyaGPT: Explain my benefits")

col1, col2 = st.columns(2)

openai_api_key = os.environ["OPENAI_KEY"]

col1, col2 = st.columns(2)
with col1:
    uploaded_files = st.file_uploader("Upload your SBC", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        # st.write("filename:", uploaded_file.name)
        with open("example.pdf", 'wb') as f: 
            f.write(bytes_data)

with col2:
    option_tone = st.selectbox(
        'What tone would you prefer?',
        ('Friendly', 'Simple', 'Verbose'))

def get_text():
    input_text = st.text_area(label="Question Input", label_visibility='collapsed', placeholder="I want to know about...", key="question_input")
    return input_text

question_input = get_text()

if len(question_input.split(" ")) > 700:
    st.write("Please enter a shorter question. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.topic_input = "What is my family deductible?"

st.button("*See an Example*", type='secondary', help="Click to see an example of a question", on_click=update_text_with_example)

st.divider()
st.markdown("#### Response:")

def qa(file, query, chain_type, k):
    loader = PyPDFLoader(file)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(texts, embeddings)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(), chain_type=chain_type, retriever=retriever, return_source_documents=True)
    result = qa({"query": query})
    print(result['result'])
    return result

if question_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    from glob import glob
    print(glob("*.pdf"))
    result = qa("example.pdf", question_input, "stuff", 3)
    
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)
    prompt_with_topic = prompt.format(response_input=str(result['result']), tone=option_tone)
    response = llm(prompt_with_topic)

    st.write(response)