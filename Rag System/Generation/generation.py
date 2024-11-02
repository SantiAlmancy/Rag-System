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


# Example of usage
# Define the question to be rephrased
client = initializeModelAPI()
question = "What were the design inspirations behind the Williams Mercedes FW43B's new livery in 2021?"
#question = "What is the capital of France?"
context = """Williams Racing proudly launches its 2021 Formula One challenger, the Williams Mercedes FW43B, featuring a striking new livery for the season ahead. The team’s new look captures the spirit of the team’s past, the present transformation and its drive to future ambitions as it heads into its first full season of ownership under US based Investment company, Dorilton Capital.
Whilst evolutionary on the technical side due to the regulations, hence the designation FW43B as opposed to the FW44, the 2021 car will race with a dramatic new visual identity sporting a livery inspired by Williams’ all-conquering cars of the 1980s and 1990s, combining blues, white and yellow accents.

Williams Racing is proud to reveal the livery that will adorn the FW45, the team’s new challenger for the 2023 FIA Formula One World Championship season. Williams Racing is also thrilled to showcase major partners, with Gulf Oil, Stephens, Michelob ULTRA and 
PureStream joining the team from the 2023 season.
The 2023 livery design is an evolution of the FW44, retaining the brand visual cues which features a contrasting diamond shape and flashes of red and blue, embodying the exciting new era of Williams Racing. This year's design features a colour finish change to matte, providing a stronger on track visual.

Williams Racing is proud to reveal the livery that will adorn the FW44, the team’s vibrant new challenger for the 2022 FIA Formula One season. The design, featuring a contrasting diamond shape and flashes of red and blue, embodies the exciting new era of the 
Williams brand, whilst still retaining the classic team spirit.

Williams Racing proudly launches its 2021 Formula One challenger, the Williams Mercedes FW43B, featuring a striking new livery for the season ahead. The team’s new look captures the spirit of the team’s past, the present transformation and its drive to future ambitions as it heads into its first full season of ownership under US based Investment company, Dorilton Capital.
Whilst evolutionary on the technical side due to the regulations, hence the designation FW43B as opposed to the FW44, the 2021 car will race with a dramatic new visual identity sporting a livery inspired by Williams’ all-conquering cars of the 1980s and 1990s, combining blues, white and yellow accents.
"""
print(generateResponse(client, context ,question, 1))