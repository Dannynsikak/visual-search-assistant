
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB client and collection
client = chromadb.Client()
collection = client.get_or_create_collection("image_descriptions")

# Load model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text):
    return model.encode([text])[0]

def add_to_database(item_id, description):
    # Check if ID already exists
    existing_ids = collection.get(ids=[item_id])
    if existing_ids:
        print(f"Embedding ID {item_id} already exists. Skipping addition.")
        return

    embedding = generate_embedding(description)
    collection.add(ids=[item_id], embeddings=[embedding], metadatas=[{'description': description}])
    print(f"Embedding ID {item_id} added successfully.")


def query_database(query_text):
    query_embedding = generate_embedding(query_text)
    results = collection.query(query_embeddings=[query_embedding], n_results=5)
    return results
