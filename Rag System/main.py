import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from Routing.routing import *
from QueryConstruction.qcVectorStore import *
from Generation.generation import *
from sentence_transformers import util

def initializeModelAPI():
    # Load environment variables
    load_dotenv()
    apiToken = os.getenv("API_TOKEN")

    # Initialize the client for Hugging Face Inference API with a specific API key
    client = InferenceClient(api_key=apiToken)
    return client

def loadRetriever():
    RETRIEVER_PATH = os.getenv("RETRIEVER_PATH")
    with open(RETRIEVER_PATH, "rb") as f:
        return pickle.load(f)
    
def generateUniqueDocs(docs):
    # Remove duplicate documents and returns a list of unique documents.
    uniqueDocs = []
    seenDocs = set()  # Use a set to track seen documents

    for doc in docs:
        if doc.page_content not in seenDocs:
            seenDocs.add(doc.page_content)
            uniqueDocs.append(doc)

    return uniqueDocs

def docsToString(docs):
    # Converts the list of documents into a single string.
    docsText = ""
    for doc in docs:
        docsText += f"Retrieved Document:\nText: {doc.page_content}\n\n"
    return docsText

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

    # Vector store case
    if (mostCommonRoute == 1):
        # Retrieval and processing
        retriever = loadRetriever()
        allDocs = []

        # Retrieve documents for each question variation
        for variation in questionVariations:
            docs = retriever.get_relevant_documents(variation)
            allDocs.extend(docs)  # Add retrieved documents to the total list

        # Remove duplicate documents
        uniqueDocs = generateUniqueDocs(allDocs)

        # Convert unique documents to a string format
        retrievedDocsText = docsToString(uniqueDocs)

        # Print the text of the unique documents
        print(retrievedDocsText)
        print(generateResponse(client, retrievedDocsText ,question, mostCommonRoute))

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
