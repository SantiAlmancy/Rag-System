from scipy.spatial.distance import cosine
from fuzzywuzzy import fuzz
import pickle
    
def getEmbedding(embedModel, text):
    return embedModel.embed_query(text)

def isSpecificModelSimilar(embedModel, query, topics, threshold=0.70, fuzzThreshold=70):
    # Generate embedding for the query once
    queryEmbedding = getEmbedding(embedModel, query)

    for topic in topics:
        # Check approximate match with fuzzy score
        fuzzyScore = fuzz.partial_ratio(query.lower(), topic.lower())
        if fuzzyScore >= fuzzThreshold:
            topicEmbedding = getEmbedding(embedModel, topic)
            similarity = 1 - cosine(queryEmbedding, topicEmbedding)  # Cosine similarity

            if similarity >= threshold:
                return True  # High match found

    return False  # No relevant match found

def promptModelCheck(client, query, topics1, topics2, modelName="mistralai/Mistral-7B-Instruct-v0.3"):
    # Create a message to check if the question relates to the specified topics
    messages = [
        {
            "role": "user",
            "content": f"""
            You are a Formula 1 (F1) expert tasked with determining whether a given data source contains sufficient information to answer questions about F1 topics. You possess extensive knowledge of drivers, teams, races, and Formula 1 cars from 1950 onward.

            When analyzing a question, follow these steps for each word in the question:

            1. **Categorize the Question**: Identify if it falls under one of the following categories:
            - **Drivers**: Names of Formula 1 drivers or related terms.
            - **Races**: Names of races, Grand Prix events, or race positions.
            - **Technology/Vehicle**: Terms related to Formula 1 cars, technology, innovations, or car parts.

            2. **Determine Relevance**: Based on your analysis, assess whether the question relates to one of the following options or any related topics:
            - **Option 1**: Topics related to Formula 1 Technology/Vehicle.
            - **Option 2**: Topics related to Formula 1 Drivers and/or Races.

            **Topics for consideration**:
            - **Option 1 Topics**: {", ".join(topics1)}
            - **Option 2 Topics**: {", ".join(topics2)}

            3. **Evaluate Relatedness**: Determine if the identified topics in the question are at least somewhat related to the topics in the provided options. If they are, assign the question to either Option 1 or Option 2 accordingly.

            4. **Synonym Analysis**: Analyze the question for synonyms that may relate closely to the relevant topics. If they do, assign the question to either Option 1 or Option 2 accordingly.

            Respond with:
            - "1" if the question pertains to Option 1 topics, similar topics to Option 1, or synonyms related to Option 1 topics.
            - "2" if the question pertains to Option 2 topics, similar topics to Option 2, or synonyms related to Option 2 topics.
            - "no" if neither applies.

            *Question*: "{query}"
            """
        }
    ]

    response = client.chat.completions.create(
        model=modelName,
        messages=messages,
        max_tokens=5,
        stream=True
    )

    answer = ""
    for chunk in response:
        answer += chunk.choices[0].delta.content

    normalizedAnswer = answer.strip().lower()
    if "1" in normalizedAnswer:
        return 1  # Matches Option 1
    elif "2" in normalizedAnswer:
        return 2  # Matches Option 2
    else:
        return 0  # Matches neither

def routingRag(embedModel, client, query, topics):
    # Step 1: Check if the specific vehicle model is similar
    if isSpecificModelSimilar(embedModel, query, topics):
        return 1

    # Step 2 and 3: Check if the query is related to specific topics
    topicsOption1 = [
        "Formula 1 (F1) cars",
        "Formula 1 (F1) vehicles"
        "Formula 1 (F1) technology",
        "Formula 1 (F1) innovations",
        "Formula 1 (F1) curiosities",
    ]
    topicsOption2 = [
        "Formula 1 (F1) Drivers",
        "Formula 1 (F1) Participations"
        "Formula 1 (F1) Races",
        "Formula 1 (F1) Positions",
        "Formula 1 (F1) Wins"
        "Formula 1 (F1) Grand Prix",
    ]

    # Call the model check function
    return promptModelCheck(client, query, topicsOption1, topicsOption2)