from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from vector_database import faiss_db
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

# LLM (Gemini Pro)
llm_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-04-17",
    google_api_key=api_key,
    temperature=0.7
)

# Retrieve docs
def retrieve_docs(query):
    return faiss_db.similarity_search(query)

def get_context(documents):
    return "\n\n".join([doc.page_content for doc in documents])

# Answer query
custom_prompt_template = """
You are an expert assistant for DGCA Civil Aviation Requirements (CAR) regulations.
Answer the operator's question using only the information provided in the context.
Be clear, detailed, and professional in your response.
If you don't know the answer, say "I don't know" and do not invent anything.

Question: {question}
Context: {context}

Answer:
"""

def answer_query(documents, model, query):
    context = get_context(documents)
    prompt = ChatPromptTemplate.from_template(custom_prompt_template)
    chain = prompt | model
    return chain.invoke({"question": query, "context": context}).content
