from scipy.spatial.distance import cosine
from fuzzywuzzy import fuzz
import pickle

# Load embeddings from the .pkl file
def loadEmbeddings(embeddingsPath):
    with open(embeddingsPath, "rb") as file:
        return pickle.load(file)
    
def getEmbedding(embedModel, text):
    return embedModel.embed_query(text)

def isSpecificModelSimilar(embedModel, query, topics, threshold=0.8, fuzzThreshold=95):
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

def promptModelCheck(client, query, topics1, topics2, modelName="mistralai/Mixtral-8x7B-Instruct-v0.1"):
    # Create a message to check if the question relates to the specified topics
    messages = [
        {
            "role": "user",
            "content": f"""
            You are an AI designed to determine if a Formula 1 (F1) data source has enough information to answer questions about F1 topics. 
            You understand the context of F1, including drivers, circuits, teams, and race events from 1950 and onwards, and the information such as names and details.

            When analyzing the question, remember that:
            1. **Drivers** are key participants in F1 and their details (e.g., wins, personal information) are important.
            2. **Races** provide context about events and results, including specific wins and statistics.
            3. **Circuits** are venues where races occur and can influence results.
            4. **Technology** are innovations from F1 teams to improve their vehicles, includes vehicle component, mechanism and form improvements.
            5. Your understanding of these aspects should guide your assessment. 
            6. For each word in the question, determine if it pertains to a driver, race, circuit, or technology. If a relevant term is identified, analyze it in relation to the associated topics.
            Evaluate whether the question relates to the following options:
            - **Option 1**: {topics1} (Data source only from 2000 and onwards, discard if it includes any other year)
            - **Option 2**: {topics2} (Data source only from 1950 and onwards, discard if it includes any other year)

            Please respond with:
            - "1" if the question relates to Option 1,
            - "2" if it relates to Option 2, or
            - "no" if neither applies.

            **Question**: "{query}"
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
        "General information on Formula 1 vehicles",
        "Vehicle technology and innovations for Formula 1",
        "Formula 1 car models"
    ]
    topicsOption2 = {
        "Drivers": ["Drivers participate in races.", "Drivers have standings based on their performance.", "Drivers win races in various years.", "Drivers have personal information (number, surname, code, forename, date of birth)."],
        "Races": ["Races are conducted on circuits.", "Races result in wins for drivers.", "Races have name and date."],
        "Circuits": ["Circuits host multiple races.", "Different circuits have different characteristics such as name and location."],
        "Standings": ["Each driver has a standing for a race.", "A race is won by a driver."]
    }

    # Call the model check function
    return promptModelCheck(client, query, topicsOption1, topicsOption2)
