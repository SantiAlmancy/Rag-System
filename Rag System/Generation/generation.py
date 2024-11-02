from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

def generateResponseVectorStore(client, context, question):
    # Define the messages to send to the AI, including instructions and the user's question
    messages = [
        {
            "role": "system",
            "content": """Using the information contained in the context,
            give a comprehensive answer to the question.
            Respond only to the question asked, response should be concise and relevant to the question.
            If the answer cannot be deduced from the context, answer with 'I don't know'"""
        },
        {
            "role": "user",
            "content": f"""Context:
            {context}
            ---
            Now here is the question you need to answer.

            Question: {question}"""
        }
    ]

    # Send a chat completion request to the model, setting parameters like max tokens and streaming response
    stream = client.chat.completions.create(
        # Specify the model to use; this line can be adjusted to test different models
        model="mistralai/Mixtral-8x7B-Instruct-v0.1", 
        messages=messages, 
        max_tokens=500,
        stream=True
    )

    answer = ""
    for chunk in stream:
        answer += chunk.choices[0].delta.content

    return answer

def generateResponse(client, context, question, pathNumber):
    response = ""
    if pathNumber == 1:
        response = generateResponseVectorStore(client, context, question)
    elif pathNumber == 2:
        response = "GraphQL"
    return response
