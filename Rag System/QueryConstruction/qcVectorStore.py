from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
apiToken = os.getenv("API_TOKEN")

# Initialize the client for Hugging Face Inference API with a specific API key
client = InferenceClient(api_key=apiToken)

# Define the question to be rephrased
question = "How does the new leadership at Williams Racing influence the vision and direction for the FW43B?"

# Define the messages to send to the AI, including instructions and the user's question
messages = [
    { 
        "role": "user", 
        "content": f"""You are an AI language model assistant tasked with generating informative queries for a vector search engine.
        The user has a question: "{question}"
        Your goal is to create three variations of this question that capture different aspects of the user's intent. These variations will help the search engine retrieve relevant documents even if they don't use the exact keywords as the original question.
        Provide these alternative questions, each on a new line.
        Original question: {question}""" 
    }
]

# Send a chat completion request to the model, setting parameters like max tokens and streaming response
stream = client.chat.completions.create(
    # Specify the model to use; this line can be adjusted to test different models
    # model="meta-llama/Llama-3.2-3B-Instruct", 
    model="mistralai/Mistral-7B-Instruct-v0.3",
    messages=messages, 
    max_tokens=300,
    stream=True
)

# Accumulate the response parts from the streamed output
response_parts = []
for chunk in stream:
    # Append each chunk's content to the response parts list
    response_parts.append(chunk.choices[0].delta.content)

# Join all response parts into a single string and print the final response
full_response = "".join(response_parts)
print(full_response)