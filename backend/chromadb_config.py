import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

<<<<<<< HEAD

# Initialize ChromaDB client and collection
client = chromadb.Client()
collection = client.get_or_create_collection("image_descriptions")
user_history_collection = client.get_or_create_collection("UserHistory")
=======
# Initialize ChromaDB client and collection
client = chromadb.Client()
collection = client.get_or_create_collection("image_descriptions")
>>>>>>> 221de2e8fc6779426901f2f3eb86618b73e0c2c2

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
<<<<<<< HEAD
        padding = np.zeros(target_length - len(embedding))
=======
        padding = [0] * (target_length - len(embedding))
>>>>>>> 221de2e8fc6779426901f2f3eb86618b73e0c2c2
        return np.concatenate([embedding, padding])

def generate_embedding(text):
    """
    Generate an embedding for the given text using the SentenceTransformer model,
    with padding for consistency across embeddings.
    """
<<<<<<< HEAD
    embedding = np.array(model.encode([text])[0])
=======
    embedding = model.encode([text])[0]
>>>>>>> 221de2e8fc6779426901f2f3eb86618b73e0c2c2
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
<<<<<<< HEAD
        if existing_ids["metadatas"]:
=======
        if existing_ids:
>>>>>>> 221de2e8fc6779426901f2f3eb86618b73e0c2c2
            print(f"Embedding ID {item_id} already exists. Skipping addition.")
            return
    except Exception:
        # ID does not exist, safe to proceed
        pass

    # Generate embedding and add to the collection
    embedding = generate_embedding(description)
<<<<<<< HEAD
    collection.add(ids=[item_id], embeddings=[embedding], metadatas=[{'description': description,}])
    print(f"Embedding ID {item_id} added successfully.")
=======
    collection.add(ids=[item_id], embeddings=[embedding], metadatas=[{'description': description}])
    print(f"Embedding ID {item_id} added successfully.")

def query_database(query_text):
    """
    Query the ChromaDB collection with a text input and return the top 5 most similar items.
    """
    query_embedding = generate_embedding(query_text)
    results = collection.query(query_embeddings=[query_embedding], n_results=5)
    
    # Format results for readability
    formatted_results = [
        {"id": result["id"], "description": result["metadata"]["description"]}
        for result in results
    ]
    return formatted_results
>>>>>>> 221de2e8fc6779426901f2f3eb86618b73e0c2c2
