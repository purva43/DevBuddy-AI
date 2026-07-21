import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="devbuddy_knowledge")

def add_document(doc_id: str, text: str):
    """Store a piece of text in the vector database."""
    collection.add(
        ids=[doc_id],
        documents=[text]
    )

def search(query: str, n_results: int = 2):
    """Find the most semantically relevant stored documents for a query."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results["documents"][0]