import os
import pickle
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()
RETRIEVER_PATH = os.getenv("RETRIEVER_PATH")
API_TOKEN = os.getenv("API_TOKEN")

# Initialize embedding model
model = SentenceTransformer("hkunlp/instructor-base")

# Initialize InferenceClient with authentication token
client = InferenceClient(api_key=API_TOKEN)

# Step 1: Load retriever from file
def load_retriever():
    with open(RETRIEVER_PATH, "rb") as f:
        return pickle.load(f)

# Step 2: Check cosine similarity in vector store
def search_vector_store(query, retriever, threshold=0.95):
    docs = retriever.get_relevant_documents(query)
    if docs:
        query_emb = model.encode(query, convert_to_tensor=True)
        doc_emb = model.encode(docs[0].page_content, convert_to_tensor=True)
        cosine_similarity = util.cos_sim(query_emb, doc_emb).item()
        print(cosine_similarity)
        return cosine_similarity >= threshold
    return False
