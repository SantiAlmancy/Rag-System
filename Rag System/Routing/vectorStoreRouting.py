import pandas as pd

def loadTopics(topicsPath):
    # Topics from CSV
    df = pd.read_csv(topicsPath)
    return df["Name"].tolist()  # Return list of topics

def canAnswerWithVectorStore(client, query, topics):
    # Prompt for the model
    messages = [
        {
            "role": "user",
            "content": f"""
            You are an AI tasked with determining if a set of topics provides enough context to answer a question.
            Focus exclusively on the following vehicle-related topics: {', '.join(topics)}.
            Can you answer the question based on these topics? Respond with "yes" if the question is specifically about Formula 1 vehicles, including their specifications, history, or curiosities from 2000 onwards. Respond with "no" if it relates to drivers or any other non-vehicle topics.
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
    return normalized_answer.startswith('yes') # True if the model says 'yes'
