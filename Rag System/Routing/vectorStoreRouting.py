import pandas as pd

def loadTopics(topicsPath):
    # Load topics from CSV
    df = pd.read_csv(topicsPath)
    return df["Name"].tolist()  # Return list of topics

def canAnswerWithVectorStoreUsingModel(client, query, topics):
    # Prepare the prompt for the model
    messages = [
        {
            "role": "user",
            "content": f"""
            You are an AI tasked with determining if a set of topics provides enough context to answer a question.
            Topics include: {', '.join(topics)}.
            Can you answer the question based on these topics? Respond with "yes" or "no" only.
            Additionally, respond "yes" if the question is about the history or curiosities of Formula 1 vehicles from 2000 onwards.
            Question: "{query}"
            """
        }
    ]

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.2-3B-Instruct",
        messages=messages,
        max_tokens=10,
        stream=True
    )

    # Get response content
    answer = ""
    for chunk in response:
        answer += chunk.choices[0].delta.content

    return answer.strip().lower() == 'yes'  # Return True if the model says 'yes'
