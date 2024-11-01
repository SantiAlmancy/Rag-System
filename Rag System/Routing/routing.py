import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from vectorStoreRouting import *
from graphRouting import *

def routeQuery(query):
    load_dotenv()
    processedDataPath = os.getenv("PROCESSED_DATA_PATH")

    topics = loadTopics(processedDataPath)

    # Initialize the model client
    API_TOKEN = os.getenv("API_TOKEN")
    client = InferenceClient(api_key=API_TOKEN)

    # Check vector store
    if canAnswerWithVectorStore(client, query, topics):
        return 1  # Vector store can answer

    # Check graph
    if canAnswerWithGraph(client, query):
        return 2  # Graph can answer

    return 0  # None can answer

# Example
print(routeQuery("Which Williams Mercedes FW43B 2021 livery concept was inpired by classic racing livery patterns?"))