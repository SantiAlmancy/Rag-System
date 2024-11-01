def canAnswerWithGraphUsingModel(client, query):
    # Fixed topics
    topics = ["Formula 1 drivers", "Formula 1 driver standings", "Formula 1 circuits", "Formula 1 races"]
    
    # Prompt for the model
    messages = [
        {
            "role": "user",
            "content": f"""
            You are an AI tasked with determining if a graph can provide enough information to answer a question.
            Topics include: {', '.join(topics)}.
            Can you answer the question based on the graph? Respond with "yes" or "no" only.
            Question: "{query}"
            """
        }
    ]

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.2-3B-Instruct",
        messages=messages,
        max_tokens=5,
        stream=True
    )

    # Response content
    answer = ""
    for chunk in response:
        answer += chunk.choices[0].delta.content

    return answer.strip().lower() == 'yes'  # True if the model says 'yes'
