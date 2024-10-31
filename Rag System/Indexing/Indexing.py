# Import modules
import os
import pandas as pd
import pickle  # Import pickle for serialization
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Load CSV file path from environment variable
    DATA_PATH = os.getenv("DATA_PATH")
    df = pd.read_csv(DATA_PATH)

    # Initialize HuggingFace embedding model
    embed_model = HuggingFaceEmbeddings(model_name="hkunlp/instructor-base")

    # Set chunk size and overlap
    chunk_size = 700        # Max characters per chunk
    chunk_overlap = 50      # Overlap between chunks

    # Create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    # Split text into chunks
    split_texts = []
    for _, row in df.iterrows():
        splits = text_splitter.split_text(row['Text'])
        split_texts.extend(splits)

    # Create embeddings for all chunks and store in FAISS vectorstore
    split_texts_embeddings = [(text, embed_model.embed_query(text)) for text in split_texts]
    

if __name__ == "__main__":
    main()
