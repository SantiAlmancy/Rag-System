from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

def generateQuestionVariations(client, question):
    # Define the messages to send to the AI, including instructions and the user's question
    messages = [
        { 
            "role": "user", 
            "content": f"""You are an AI language model assistant tasked with generating informative queries for a vector search engine.
            The user has a question: "{question}"
            Your goal is to create three simple variations of this question that capture different aspects of the user's intent. These variations will help the search engine retrieve relevant documents even if they don't use the exact keywords as the original question.
            Provide only these alternative questions as output without any enumeration or listing symbols, just present each one on a new line.
            Original question: {question}""" 
        }
    ]

    # Send a chat completion request to the model, setting parameters like max tokens and streaming response
    stream = client.chat.completions.create(
        # Specify the model to use; this line can be adjusted to test different models
        #model="mistralai/Mixtral-8x7B-Instruct-v0.1", 
        model="meta-llama/Llama-3.2-3B-Instruct",
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

    # Split the response into a list of questions by line breaks and remove empty lines
    questionList = [q.strip() for q in fullResponse.splitlines() if q.strip()]
    return questionList
