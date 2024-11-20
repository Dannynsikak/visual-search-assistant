import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize ChromaDB client and collection
client = chromadb.Client()
collection = client.get_or_create_collection("image_descriptions")

# Load model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# **Function to normalize embeddings**: Scales embeddings to unit length
def normalize_embedding(embedding):
    norm = np.linalg.norm(embedding)
    if norm == 0:
        return embedding
    return embedding / norm

# **Function to add padding to embeddings**: Ensures all embeddings have consistent dimensions
def pad_embedding(embedding, target_length=384):
    if len(embedding) >= target_length:
        return embedding[:target_length]
    else:
        # Padding with zeros if the embedding is shorter than the target length
        padding = [0] * (target_length - len(embedding))
        return np.concatenate([embedding, padding])

def generate_embedding(text):
    """
    Generate an embedding for the given text using the SentenceTransformer model,
    with padding for consistency across embeddings.
    """
    embedding = model.encode([text])[0]
    normalized_embedding = normalize_embedding(embedding)
    padded_embedding = pad_embedding(normalized_embedding)
    return padded_embedding

def add_to_database(item_id, description):
    """
    Add an item to the ChromaDB collection with a unique ID and embedding of the description.
    Checks if the ID already exists to prevent duplicates.
    """
    # Check if ID already exists
    try:
        existing_ids = collection.get(ids=[item_id])
        if existing_ids:
            print(f"Embedding ID {item_id} already exists. Skipping addition.")
            return
    except Exception:
        # ID does not exist, safe to proceed
        pass

    # Generate embedding and add to the collection
    embedding = generate_embedding(description)
    collection.add(ids=[item_id], embeddings=[embedding], metadatas=[{'description': description}])
    print(f"Embedding ID {item_id} added successfully.")
