# PDF Chatbot

A lightweight RAG-powered PDF assistant built with Python and Streamlit. Upload a PDF, extract its text, convert it into searchable chunks, and ask questions about the document using a retrieval-augmented generation (RAG) workflow powered by a Gemini model.

## Features

- Upload a PDF from the browser
- Extract text content from the document
- Split long documents into manageable chunks
- Build a vector database for semantic retrieval
- Ask natural-language questions grounded in the uploaded PDF
- Get responses generated using the configured LLM

## Tech Stack

- Python
- Streamlit
- PyPDF
- SentenceTransformers
- ChromaDB
- Google Generative AI

## Project Structure

```text
.
├── app.py
├── .env.example
├── requirements.txt
├── modules/
│   ├── __init__.py
│   ├── embedding.py
│   ├── llm.py
│   ├── pdf_utils.py
│   └── vectordb.py
├── prompt/
│   └── rag_prompt.txt
└── README.md
```

## Prerequisites

- Python 3.10+
- A Google AI API key with access to Gemini
- Internet access for downloading the embedding model and model dependencies

## Setup

1. Clone the repository

```bash
git clone https://github.com/habiba11111/Project.git
cd Project
```

2. Create a virtual environment

```bash
python -m venv .venv
```

3. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Add your API key

Create a `.env` file in the project root using the example:

```bash
copy .env.example .env
```

Then update `.env` with your key:

```env
GOOGLE_API_KEY=your_api_key_here
```

## Run the App

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).

## How It Works

1. The uploaded PDF is read using `PyPDF`.
2. Text is split into smaller chunks for efficient processing.
3. Each chunk is embedded using a sentence-transformer model.
4. ChromaDB stores the embeddings and metadata.
5. The user question is embedded and matched against stored chunks.
6. The retrieved context is sent to Gemini with the prompt template.
7. The model generates an answer based strictly on the PDF content.

## Notes

- This project works best with text-based PDFs.
- For scanned/image-only PDFs, OCR would be needed before extraction.
- The assistant answers only from retrieved context; if the answer is not present, it returns a fallback message from the prompt template.

## License

This project is provided for educational and experimental use.

