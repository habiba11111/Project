import hashlib
from io import BytesIO

import streamlit as st

from modules.llm import load_model
from modules.langchain import build_retrieval

model = load_model()

st.set_page_config(page_title="PDF Chat", page_icon="📚", layout="centered")

st.markdown(
    """
    <style>
    :root {
        --page: #f5efe5;
        --surface: #fffdf8;
        --surface-alt: #eee3d2;
        --ink: #35251b;
        --muted: #655144;
        --brown: #68452f;
        --brown-hover: #523522;
        --border: #cdb9a2;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--page);
        color: var(--ink);
    }
    [data-testid="stHeader"] {
        background: rgba(245, 239, 229, 0.94);
    }
    [data-testid="stMain"] {
        color: var(--ink);
    }
    [data-testid="stMain"] .block-container {
        max-width: 860px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3, p, li, label, [data-testid="stMarkdownContainer"],
    [data-testid="stCaptionContainer"], [data-testid="stWidgetLabel"] {
        color: var(--ink) !important;
        overflow-wrap: anywhere;
    }
    h1 {
        letter-spacing: -0.035em;
        line-height: 1.15;
    }
    [data-testid="stCaptionContainer"] {
        color: var(--muted) !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background: var(--surface);
        border: 1px dashed var(--border);
        border-radius: 14px;
    }
    [data-testid="stFileUploaderDropzone"] * {
        color: var(--ink) !important;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background: var(--surface-alt);
        border: 1px solid var(--border);
        color: var(--ink) !important;
    }
    input, textarea, [data-baseweb="input"], [data-baseweb="textarea"] {
        background: var(--surface) !important;
        color: var(--ink) !important;
        border-color: var(--border) !important;
    }
    input::placeholder, textarea::placeholder {
        color: var(--muted) !important;
        opacity: 1;
    }
    [data-testid="stForm"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1rem;
    }
    [data-testid="stFormSubmitButton"] button,
    [data-testid="stButton"] button {
        background: var(--brown);
        border: 1px solid var(--brown);
        color: #fffdf8 !important;
        border-radius: 9px;
        font-weight: 600;
    }
    [data-testid="stFormSubmitButton"] button:hover,
    [data-testid="stButton"] button:hover {
        background: var(--brown-hover);
        border-color: var(--brown-hover);
        color: #fffdf8 !important;
    }
    [data-testid="stAlert"] {
        border-radius: 12px;
    }
    [data-testid="stChatMessage"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
    }
    [data-testid="stChatMessage"] * {
        color: var(--ink) !important;
        overflow-wrap: anywhere;
    }
    a {
        color: var(--brown) !important;
    }
    @media (max-width: 640px) {
        [data-testid="stMain"] .block-container {
            padding: 1.25rem 1rem 2rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="padding: 0.5rem 0 1.25rem;">
        <p style="color: #68452f !important; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase;">
            Your reading companion
        </p>
        <h1 style="margin: 0;">Chat with your PDF</h1>
        <p style="font-size: 1.08rem; color: #655144 !important; margin-top: 0.65rem;">
            Upload a document, ask a question, and get an answer grounded in its content.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("1. Choose a document")
uploaded_file = st.file_uploader(
    "Select a PDF to get started",
    type=["pdf"],
    help="Choose a text-based PDF. Your document stays in this app session.",
)

if uploaded_file is None:
    st.info("Your document and question box will appear here once you upload a PDF.")
else:
    retrieval = build_retrieval(uploaded_file)

    st.subheader("2. Ask a question")
    user_question = st.text_area(
        "Type your question here",
        placeholder="What is the main topic of this document?",
        height=100,
    )

    if user_question:
        with st.spinner("Generating answer..."):
            # Retrieve relevant documents from the vector store
           relevant_docs = retrieval.invoke(user_question)

            # Combine the content of the relevant documents into a single context string
           context = "\n\n".join([doc.page_content for doc in relevant_docs])

            # Generate a response using the LLM model
           response = model.invoke(f"Context: {context}\n\nQuestion: {user_question}")

           st.subheader("Answer")
           st.write(response.content)