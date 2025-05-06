import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()
google_api_key = os.environ.get("GOOGLE_API_KEY")

custom_prompt_template = """
You are an expert assistant for DGCA Civil Aviation Requirements (CAR) regulations.
Answer the operator's question using only the information provided in the context.
Be clear, detailed, and professional in your response.
If you don't know the answer, say "I don't know" and do not invent anything.

Question: {question}
Context: {context}

Answer:
"""

# Model and paths
FAISS_DB_PATH = "vectorstore/db_faiss"
PDFS_DIR = "pdfs/"
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)
llm_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17", google_api_key=google_api_key, temperature=0.3)

# Functions
def upload_pdf(file):
    with open(PDFS_DIR + file.name, "wb") as f:
        f.write(file.getbuffer())

def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    return loader.load()

def create_chunks(documents): 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    return text_splitter.split_documents(documents)

def create_vector_store(db_path, text_chunks):
    faiss_db = FAISS.from_documents(text_chunks, embedding_model)
    faiss_db.save_local(db_path)
    return faiss_db

def retrieve_docs(faiss_db, query):
    return faiss_db.similarity_search(query)

def get_context(docs):
    return "\n\n".join([doc.page_content for doc in docs])

def answer_query(documents, model, query):
    context = get_context(documents)
    prompt = ChatPromptTemplate.from_template(custom_prompt_template)
    chain = prompt | model
    response = chain.invoke({"question": query, "context": context})
    return response.content

# Streamlit UI
st.set_page_config(page_title="DGCA CAR Assistant", layout="centered")
st.title("🛫 DGCA CAR Regulations Assistant")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Upload DGCA CAR PDF", type="pdf")
user_query = st.text_area("Ask your DGCA-related query:", height=150, placeholder="E.g. What are the requirements for Air Operator Permit renewal?")

if st.button("Ask Assistant"):
    if uploaded_file and user_query:
        upload_pdf(uploaded_file)
        documents = load_pdf(PDFS_DIR + uploaded_file.name)
        text_chunks = create_chunks(documents)
        faiss_db = create_vector_store(FAISS_DB_PATH, text_chunks)
        retrieved_docs = retrieve_docs(faiss_db, user_query)
        response = answer_query(retrieved_docs, llm_model, user_query)

        # Store conversation in session state
        st.session_state.chat_history.append(("user", user_query))
        st.session_state.chat_history.append(("assistant", response))

    else:
        st.error("Please upload a DGCA CAR PDF and enter your question.")

# Display chat history
for sender, message in st.session_state.chat_history:
    st.chat_message(sender).write(message)
