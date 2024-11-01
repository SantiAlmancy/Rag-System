import os

def canAnswerWithGraph(client, query):
    # Load the ontology from the .ttl file specified in the environment variable
    ttl_file_path = os.getenv("K_GRAPH_ONTOLOGY")
    
    # Read the contents of the .ttl file
    with open(ttl_file_path, 'r', encoding='utf-8') as file:
        ttl_content = file.read()

    print(ttl_content)
    
    # Prompt for the model using the ttl content
    messages = [
        {
            "role": "user",
            "content": f"""
            You are an AI tasked with determining if a graph can provide enough information to answer a question.
            The graph contains the following ontology information:
            {ttl_content}
            Can you answer the question based on the graph? Respond with "yes" or "no" only.
            Question: "{query}"
            """
        }
    ]

    response = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=messages,
        max_tokens=5,
        stream=True
    )

    # Response content
    answer = ""
    for chunk in response:
        answer += chunk.choices[0].delta.content

    normalized_answer = answer.strip().lower()
    return normalized_answer.startswith('yes')  # True if the model says 'yes'
