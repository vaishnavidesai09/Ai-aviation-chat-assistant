import streamlit as st
from rag_pipeline import answer_query, retrieve_docs, llm_model

# Set Page Config
st.set_page_config(page_title="🛫 AI Aviation Chat Assistant", layout="centered")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: #2C3E50;'>🛫 AI-Powered Aviation Chat Assistant</h1>
        <p style='color: #7F8C8D; font-size: 18px;'>
            Ask about uploaded aviation documents and get real-time answers with Gemini.
        </p>
    </div>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("📄 Upload DGCA CAR PDF", type="pdf")

# Chat input
user_query = st.chat_input("Ask a question about the document...")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Process user input
if user_query:
    if not uploaded_file:
        st.error("🚫 Please upload a DGCA CAR PDF first.")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Process and respond
        with st.chat_message("assistant"):
            with st.spinner("Searching the document..."):
                retrieved_docs = retrieve_docs(user_query)
                response = answer_query(documents=retrieved_docs, model=llm_model, query=user_query)

                # Display assistant message
                st.markdown(response)  # FIXED: Removed .content
                st.session_state.messages.append({"role": "assistant", "content": response})
