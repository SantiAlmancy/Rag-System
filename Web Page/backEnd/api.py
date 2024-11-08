import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

rag_system_path = os.path.abspath(os.path.join(__file__, '../../../Rag system'))
sys.path.insert(0, rag_system_path)

from main import generateAnswer, initializeModelAPI, loadEmbeddings

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

embedModel = HuggingFaceEmbeddings(model_name="hkunlp/instructor-base")
client = initializeModelAPI()
embeddingsTopics = os.getenv("EMBEDDINGS_TOPICS")
embedTopics = loadEmbeddings(embeddingsTopics)

class QuestionRequest(BaseModel):
    question: str
    text: str

@app.post("/generate-answer")
async def generate_answer(request: QuestionRequest):
    question = request.question
    text = request.text

    try:
        result = generateAnswer(question, embedModel, client, embedTopics)
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {e}")

@app.get("/")
async def root():
    return {"message": "Welcome to the Answer Generation API"}