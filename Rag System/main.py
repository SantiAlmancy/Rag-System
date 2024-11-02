import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from Routing.routing import *
from QueryConstruction.qcVectorStore import *

def initializeModelAPI():
    # Load environment variables
    load_dotenv()
    apiToken = os.getenv("API_TOKEN")

    # Initialize the client for Hugging Face Inference API with a specific API key
    client = InferenceClient(api_key=apiToken)
    return client

def generateAnswer(question, embedModel, client, embedTopics):
    # Step 1: Generate question variations
    questionVariations = generateQuestionVariations(client, question)
    
    # Step 2: Route the question
    routingResults = []
    for variation in questionVariations:
        result = routingRag(embedModel, client, variation, embedTopics)
        routingResults.append(result)
        print(f"Variation: '{variation}' -> Route: {result}")

    # Determine the most common route
    mostCommonRoute = max(set(routingResults), key=routingResults.count)

    return mostCommonRoute

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Initialize
    embedModel = HuggingFaceEmbeddings(model_name="hkunlp/instructor-base")
    client = initializeModelAPI()    
    embeddingsTopics = os.getenv("EMBEDDINGS_TOPICS")
    embedTopics = loadEmbeddings(embeddingsTopics)
    
    while True:
        # Ask the user for a question
        userQuery = input("Please enter your question (or type 'exit' to quit): ")
        
        if userQuery.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break  # Exit the loop if the user types 'exit'
        
        # Use the new function to generate the answer
        result = generateAnswer(userQuery, embedModel, client, embedTopics)  # Pass the loaded topics
        print(f"Most common route: {result}")  # Print the most common route

