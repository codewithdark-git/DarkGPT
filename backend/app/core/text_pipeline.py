from app.core.vector_store import VectorStore

def generate_embedding(text):
    # Generate embeddings for the given text
    vector_store = VectorStore()
    embedding = vector_store.store_embedding(text)
    return embedding
