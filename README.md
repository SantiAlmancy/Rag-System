
# Formula 1 RAG System - Question Answering with Vector Store and Knowledge Graph 🏎️

This project is a Retrieval-Augmented Generation (RAG) system focused on Formula 1 topics. It utilizes a **Vector Store** and a **Knowledge Graph** to answer users' natural language questions about drivers, technology, vehicles, and historical F1 data. The integration allows for quick access to accurate information based on stored documents and semantic queries.

![WhatsApp Image 2025-07-10 at 10 36 30](https://github.com/user-attachments/assets/2ea53f55-f1bc-4b04-b522-d4a6922e4070)

## Objective 🏆

To provide F1 fans and analysts with a tool that enables detailed and contextualized answers about the sport, using a combination of vector searches and a knowledge graph.

## Architecture 🚀

The project employs **FastAPI** for the backend service of the model, allowing for dynamic queries based on the vector store and knowledge graph to retrieve high-precision answers.

## Key Technologies 💡

### Backend
- **FastAPI** - Backend framework to handle user requests and serve generated responses.
- **Hugging Face Hub** - To integrate the language model and efficiently process questions.
- **LangChain** - Provides tools for creating embeddings and queries in the vector store.
- **FAISS** - Facebook's library for vector searches, optimized for high-speed data retrieval.
- **SPARQLWrapper** - For querying the RDF knowledge graph.

### Frontend
- **React** - Interactive user interface for users to make queries and receive responses.
- **Modular components** - Efficient organization of frontend code into reusable and dynamic components.

### Other Important Technologies
- **RDFlib** - For building and manipulating the RDF knowledge graph.
- **FuzzyWuzzy** - Improves accuracy in question matching using fuzzy similarity.
- **dotenv** - Secure management of environment variables.

## Installation ⚙️

1. Ensure you have **Python 3.11** and **Node.js** for the backend and frontend dependencies.
2. Clone the repository and navigate to the root folder.
3. Set up a virtual environment and install dependencies with the following commands:

    ```bash
    python -m venv venv
    source venv/bin/activate      # On MacOS/Linux
    venv\Scripts\activate         # On Windows
    pip install -r requirements.txt
    npm install                   # For the frontend
    ```

## API Endpoint 📡

The system exposes a single endpoint for questions and conversation context.


### Answer Generation

```http
POST api/generate-answer/

```
This endpoint receives a user's question and conversation context to generate a relevant answer.

- **Request Body**:
```json
{
  "question": "How did Lotus improve their motors and aerodynamics?",
  "text": "Context ..."
}
```
- **Parameters**:
  - `question`: The prompt from the user in the chat.
  - `text`: The conversation memory as context.

#### Example Response:
```json
{
  "answer": "Lotus improved their motors and aerodynamics by implementing advanced aerodynamics techniques and enhancing engine performance through innovative design changes."
}
```

## FAQ 🤔

#### How can I run the FastAPI server?
To run the FastAPI server, use the following command:
```bash
uvicorn main:app --reload
```

#### How do I interact with the API?
You can interact with the API using tools like Postman or cURL. Simply send a POST request to the `/generate-answer/` endpoint with the required JSON body.

#### What kind of questions can I ask the system?
You can ask questions related to Formula 1 vehicles, drivers, races and some car technologies.

#### Can I use this system for other racing formats?
While this system is tailored for Formula 1, it can be adapted for other racing formats by modifying the knowledge graph and vector store with relevant data.

#### Is there a limit on the length of the question or context text?
Yes, there may be practical limits depending on the model and infrastructure. It is recommended to keep questions concise and context to a manageable size to ensure optimal performance.


## Authors
- [@SantiAlmancy](https://github.com/SantiAlmancy)
- [@SebastianItamari](https://github.com/SebastianItamari)
- [@AleDiazT](https://github.com/AleDiazT)
