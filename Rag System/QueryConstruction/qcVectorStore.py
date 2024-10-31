from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

def initializeModelAPI():
    # Load environment variables
    load_dotenv()
    apiToken = os.getenv("API_TOKEN")

    # Initialize the client for Hugging Face Inference API with a specific API key
    client = InferenceClient(api_key=apiToken)
    return client

def generateQuestionVariations(client, question):
    # Define the messages to send to the AI, including instructions and the user's question
    messages = [
        { 
            "role": "user", 
            "content": f"""You are an AI language model assistant tasked with generating informative queries for a vector search engine.
            The user has a question: "{question}"
            Your goal is to create three simple variations of this question that capture different aspects of the user's intent. These variations will help the search engine retrieve relevant documents even if they don't use the exact keywords as the original question.
            Provide only these alternative questions as a result, each on a new line.
            Original question: {question}""" 
        }
    ]

    # Send a chat completion request to the model, setting parameters like max tokens and streaming response
    stream = client.chat.completions.create(
        # Specify the model to use; this line can be adjusted to test different models
        model="meta-llama/Llama-3.2-3B-Instruct", 
        #model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=messages, 
        max_tokens=350,
        stream=True
    )

    # Accumulate the response parts from the streamed output
    responseParts = []
    for chunk in stream:
        # Append each chunk's content to the response parts list
        responseParts.append(chunk.choices[0].delta.content)

    # Join all response parts into a single string and print the final response
    fullResponse = "".join(responseParts)
    return fullResponse

# Example of usage
# Define the question to be rephrased
client = initializeModelAPI()
question = "How does the 2021 Williams FW43B reflect the team's history and future ambitions in Formula 1?"
print(generateQuestionVariations(client, question))