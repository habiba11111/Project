from sentence_transformers import SentenceTransformer

def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')
# leave as it is in langchain as we need the model to be loaded in the same way for compatibility with langchain