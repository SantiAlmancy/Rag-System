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

# Example of usage
# Define the question to be rephrased
'''
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
'''

client = initializeModelAPI()
question = "In which races did Hamilton participate and in which years?"
#question = "What is the capital of France?"
context = context = """{
    'head': {'vars': ['Race', 'Year']},
    'results': {
        'bindings': [
            {
                'Race': {'type': 'literal', 'value': 'Monaco Grand Prix'},
                'Year': {'type': 'literal', 'value': '2018'},
            },
            {
                'Race': {'type': 'literal', 'value': 'British Grand Prix'},
                'Year': {'type': 'literal', 'value': '2015'},
            },
            {
                'Race': {'type': 'literal', 'value': 'Hungarian Grand Prix'},
                'Year': {'type': 'literal', 'value': '2023'},
            }
        ]
    }
}"""
print(generateResponse(client, context, question, 2))

question = "What were Hamilton's standings in each race during the 2020 season?"
context = context = """{
    "head": {"vars": ["Race", "Position"]},
    "results": {
        "bindings": [
            {
                "Race": {"type": "literal", "value": "Austrian Grand Prix"},
                "Position": {"type": "literal", "value": "2"}
            },
            {
                "Race": {"type": "literal", "value": "British Grand Prix"},
                "Position": {"type": "literal", "value": "1"}
            },
            {
                "Race": {"type": "literal", "value": "Italian Grand Prix"},
                "Position": {"type": "literal", "value": "7"}
            }
        ]
    }
}
"""
print(generateResponse(client, context, question, 2))

question = "Which drivers finished in the top 3 positions at the Monaco Grand Prix in 2018?"
context = context = """{
    "head": {"vars": ["Driver", "Year", "Position"]},
    "results": {
        "bindings": [
            {
                "Driver": {"type": "literal", "value": "Lewis Hamilton"},
                "Position": {"type": "literal", "value": "1"}
            },
            {
                "Driver": {"type": "literal", "value": "Sebastian Vettel"},
                "Position": {"type": "literal", "value": "2"}
            },
            {
                "Driver": {"type": "literal", "value": "Max Verstappen"},
                "Position": {"type": "literal", "value": "3"}
            }
        ]
    }
}
"""
print(generateResponse(client, context, question, 2))