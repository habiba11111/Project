from pypdf import PdfReader

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file.

    Args:
        pdf_file (str): The PDF file."""

    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text = page.extract_text()
    return text


def chunk_text(text, chunk_size=500):
    """
    Splits the text into chunks of a specified size.

    Args:
        text (str): The text to be chunked.
        chunk_size (int): The size of each chunk.

    Returns:
        list: A list of text chunks.
    """
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks