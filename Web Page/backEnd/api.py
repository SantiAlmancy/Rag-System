import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

# Adjust the path to the "Rag system" directory
rag_system_path = os.path.abspath(os.path.join(__file__, '../../../Rag system'))
sys.path.insert(0, rag_system_path)

from main import generateAnswer, initializeModelAPI, loadEmbeddings

# Initialize FastAPI
app = FastAPI()

# Load environment variables
load_dotenv()

# Initialize model and client
embedModel = HuggingFaceEmbeddings(model_name="hkunlp/instructor-base")
client = initializeModelAPI()    
embeddingsTopics = os.getenv("EMBEDDINGS_TOPICS")
embedTopics = loadEmbeddings(embeddingsTopics)

# Define the request model
class QuestionRequest(BaseModel):
    question: str
    text: str

@app.post("/generate-answer")
async def generate_answer(request: QuestionRequest):
    question = request.question
    text = request.text
    print(type(question)) 

    try:
        result = generateAnswer(question, embedModel, client, embedTopics) 
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {e}")

# Welcome message
@app.get("/")
async def root():
    return {"message": "Welcome to the Answer Generation API"}
