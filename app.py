import hashlib
from io import BytesIO

import streamlit as st

from modules.llm import generate_response
from modules.pdf_utils import chunk_text, extract_text_from_pdf
from modules.vectordb import build_vector_database, return_context


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
    document_bytes = uploaded_file.getvalue()
    document_id = hashlib.sha256(document_bytes).hexdigest()

    if st.session_state.get("document_id") != document_id:
        with st.spinner("Reading your PDF and preparing it for questions..."):
            document_text = extract_text_from_pdf(BytesIO(document_bytes))
            text_chunks = chunk_text(document_text)
            st.session_state.document_id = document_id
            st.session_state.document_name = uploaded_file.name
            st.session_state.document_collection = (
                build_vector_database(text_chunks) if text_chunks else None
            )
            st.session_state.messages = []

    collection = st.session_state.document_collection
    st.success(f"Ready to explore: {st.session_state.document_name}")

    if collection is None:
        st.warning(
            "No readable text was found in this PDF. Try a text-based PDF instead of a scanned image."
        )
    else:
        st.subheader("2. Ask a question")
        with st.form("question_form", clear_on_submit=True):
            user_query = st.text_input(
                "What would you like to know?",
                placeholder="For example: What are the main points?",
            )
            submitted = st.form_submit_button("Ask about this PDF")

        if submitted:
            if not user_query.strip():
                st.warning("Enter a question before submitting.")
            else:
                with st.spinner("Finding the answer in your document..."):
                    context = return_context(user_query, collection)
                    response = generate_response(user_query, context)
                st.session_state.messages.append(
                    {"question": user_query.strip(), "answer": response}
                )

        if st.session_state.messages:
            st.subheader("Your conversation")
            for message in st.session_state.messages:
                with st.chat_message("user"):
                    st.markdown(message["question"])
                with st.chat_message("assistant"):
                    st.markdown(message["answer"])
