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
            If the answer cannot be deduced from the context, **answer with 'I don't know'**
            
            Format the response to flow naturally, as if explaining to someone who is unfamiliar with the technical details of the data.
            
            Avoid introductory phrases like "Based on the provided context"."""
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

def generateResponseGraphDB(client, context, question):
    # Define the messages to send to the AI, including instructions and the user's question
    messages = [
    {
        "role": "system",
        "content": """Using the structured information provided in the context JSON,
        generate a clear and concise answer to the question.

        If the 'bindings' array is empty, **respond with 'I don't know'**. 
        Otherwise, **assume that the information in the 'bindings' array is always the answer to the question posed**.

        Format the response to flow naturally, as if explaining to someone who is unfamiliar with the technical details of the data.

        Avoid introductory phrases like "Based on the provided context" or phrases related with confidence like "Confidence: x%".
        
        Be sure to:
        - Summarize any relevant entities and their relationships.
        - Include specific data points from the context in a way that directly supports the answer.
        - Add context or implications if they enhance understanding, but keep the answer focused and directly relevant to the question.
        """
    },
    {
        "role": "user",
        "content": f"""Context JSON:
        {context}
        ---
        Now here is the question you need to answer in a clear, natural language format.

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
        response = generateResponseGraphDB(client, context, question)
    return response