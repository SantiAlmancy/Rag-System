from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

def initializeModelAPI():
    # Load environment variables
    load_dotenv()
    apiToken = os.getenv("API_TOKEN")

    # Initialize the client for Hugging Face Inference API with a specific API key
    client = InferenceClient(api_key=apiToken)
    return client