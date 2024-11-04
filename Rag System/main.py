import os
import pickle
import io  # Importar io para manejar el flujo de bytes
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from Routing.routing import *
from QueryConstruction.qcVectorStore import *
from KnowledgeGraph.query_graph import *
from Generation.generation import *
import torch

class CPU_Unpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'torch.storage' and name == '_load_from_bytes':
            return lambda b: torch.load(io.BytesIO(b), map_location='cpu')
        else:
            return super().find_class(module, name)

def initializeModelAPI():
    load_dotenv()
    apiToken = os.getenv("API_TOKEN")
    client = InferenceClient(api_key=apiToken)
    return client

def loadEmbeddings(embeddingsPath):
    with open(embeddingsPath, "rb") as file:
        return pickle.load(file)
    
def loadRetriever():
    RETRIEVER_PATH = os.getenv("RETRIEVER_PATH")
    with open(RETRIEVER_PATH, "rb") as f:
        return CPU_Unpickler(f).load()
    
def generateUniqueDocs(docs):
    uniqueDocs = []
    seenDocs = set()

    for doc in docs:
        if doc.page_content not in seenDocs:
            seenDocs.add(doc.page_content)
            uniqueDocs.append(doc)

    return uniqueDocs

def docsToString(docs):
    docsText = ""
    for doc in docs:
        docsText += f"Retrieved Document:\nText: {doc.page_content}\n\n"
    return docsText

def generateAnswer(question, embedModel, client, embedTopics):
    questionVariations = generateQuestionVariations(client, question)
    
    routingResults = []
    for variation in questionVariations:
        result = routingRag(embedModel, client, variation, embedTopics)
        routingResults.append(result)
        print(f"Variation: '{variation}' -> Route: {result}")

    mostCommonRoute = max(set(routingResults), key=routingResults.count)
    answer = ""
    
    if (mostCommonRoute == 1):
        retriever = loadRetriever()
        allDocs = []

        for variation in questionVariations:
            docs = retriever.get_relevant_documents(variation)
            allDocs.extend(docs)

        uniqueDocs = generateUniqueDocs(allDocs)
        retrievedDocsText = docsToString(uniqueDocs)
        print(retrievedDocsText)
        answer = generateResponse(client, retrievedDocsText, question, mostCommonRoute)
        print(answer)

    elif (mostCommonRoute == 2 or routingRag(embedModel, client, question, embedTopics) == 2):
        json = query_f1_knowledge_graph(question)
        answer = generateResponse(client, json, question, mostCommonRoute)
        print(json)
        print(answer)

    else:
        answer = "The information you are looking for cannot be found on this RAG System. Sorry :("

    return answer

if __name__ == "_main_":
    load_dotenv()
    embedModel = HuggingFaceEmbeddings(model_name="hkunlp/instructor-base")
    client = initializeModelAPI()    
    embeddingsTopics = os.getenv("EMBEDDINGS_TOPICS")
    print(embeddingsTopics)
    embedTopics = loadEmbeddings(embeddingsTopics)
    
    while True:
        userQuery = input("Please enter your question (or type 'exit' to quit): ")
        
        if userQuery.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break
        
        result = generateAnswer(userQuery, embedModel, client, embedTopics)