import streamlit as st
from modules.llm import generate_response
from modules.pdf_utils import extract_text_from_pdf , chunk_text
from modules.vectordb import build_vector_database , return_context

st.title("PDF Chatbot")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file) # extract text from the uploaded PDF
    text_chunks = chunk_text(text) # split the text into smaller chunks
    collection = build_vector_database(text_chunks) # build a vector database from the text chunks

    user_query = st.text_input("Ask a question about the PDF:")
    if user_query:
        context = return_context(user_query, collection) # retrieve relevant context from the vector database
        response = generate_response(user_query, context) # generate a response using the LLM
        st.write(response) # display the response to the user