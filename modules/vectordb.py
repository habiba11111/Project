import chromadb
from modules.embedding import load_model
model = load_model()

def build_vector_database(text_chunks):
    client = chromadb.Client() # this will create a new client instance
    collection = client.get_or_create_collection(name="collection") # create a new collection in the database
    for i in range(len(text_chunks)):
        embedding = model.encode(text_chunks[i]) # encode the document text into a vector representation
        collection.upsert( 
            documents=[text_chunks[i]],
            embeddings=embedding.tolist(),
            metadatas=[{"source": "pdf"}],
            ids=[str(i)]
        ) # add the document, its embedding, metadata, and an ID to the collection
    return collection

def return_context(query, collection, top_k=1):
    query_embedding = model.encode(query) # encode the query into a vector representation
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    ) # query the collection for the most similar documents
    context = results['documents'][0] # return the most relevant documents
    return "\n\n".join(context)
