## INSTEAD OF MAKING ALL THESE .py
import tempfile
# instead of utils pdf.py
from langchain_community.document_loaders import PyPDFLoader
# instead of function chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter
# instead of vectordb.py
from langchain_community.vectorstores import chroma
from langchain_huggingface import HuggingFaceEmbeddings
# Steps:
# 1. Load the PDF file using PyPDFLoader.
# 2. Split the loaded documents into chunks using RecursiveCharacterTextSplitter.
# 3. Create a vector store from the chunks.
# 4. Retrieve answers from the vector store using the retriever.
def build_retrieval(file):
    # Create a temporary file to store the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name

    # Load the PDF file using PyPDFLoader
    loader = PyPDFLoader(temp_file_path)
    pages = loader.load()

    # Split the loaded documents into chunks using RecursiveCharacterTextSplitter
    # OVERLAP_SIZE = 200  # means that the last 200 characters of one chunk will be repeated
    # at the beginning of the next chunk
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    chunks = text_splitter.split_documents(pages)

    # Create a vector store from the chunks
    vectorstore = chroma.Chroma.from_documents(chunks,
                                            embedding=HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2'),
                                            collection_name="my_collection_langchain")
    print( vectorstore.get()['documents'])

    # retrieval of answer from the vector store
    # changes database to retriever to get the answer from the vector store
    # search_kwargs={"k": 3} means that the top 3 most similar documents will be returned
    retrieval = vectorstore.as_retriever(search_kwargs={"k": 3})

    return retrieval