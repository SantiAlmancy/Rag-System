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
    
    # Create vectorstore with (text, embedding) pairs
    vectorstore = FAISS.from_embeddings(split_texts_embeddings, embedding=embed_model)

    # Create a retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Save retriever to a file at specified path
    RETRIEVER_PATH = os.getenv("RETRIEVER_PATH")
    with open(RETRIEVER_PATH, "wb") as f:
        pickle.dump(retriever, f)
    print(f"Retriever saved to {RETRIEVER_PATH}")

    # Perform a search for relevant documents
    query = "How does the unveiling of the Mercedes-AMG F1 W09 EQ Power+ reflect the evolution of hybrid technology in Formula One and its impact on the future of high-performance models from Mercedes-AMG?"
    docs = retriever.get_relevant_documents(query)

    # Print retrieved documents
    for doc in docs:
        print("Retrieved Document:")
        print(f"Text: {doc.page_content}\n")

if __name__ == "__main__":
    main()
