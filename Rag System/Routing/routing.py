import os
import pandas as pd
from langchain.embeddings import HuggingFaceEmbeddings
from scipy.spatial.distance import cosine
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

# Initialize the embedding model
embed_model = HuggingFaceEmbeddings(model_name="hkunlp/instructor-base")
client = None  # Will be initialized later

def initialize_inference_client(api_token):
    global client
    client = InferenceClient(api_key=api_token)

def load_topics(topics_path):
    # Load car model names from a CSV file
    df = pd.read_csv(topics_path)
    return df["Name"].tolist()  # Return a list of model names

def get_embedding(text):
    # Generate embedding for the given text
    return embed_model.embed_query(text)

def is_specific_model_similar(query, topics, threshold=0.8, fuzz_threshold=80):
    # Generate embedding for the query once
    query_embedding = get_embedding(query)

    for topic in topics:
        # Check approximate match with fuzzy score
        fuzzy_score = fuzz.partial_ratio(query.lower(), topic.lower())
        if fuzzy_score >= fuzz_threshold:
            topic_embedding = get_embedding(topic)
            similarity = 1 - cosine(query_embedding, topic_embedding)  # Cosine similarity

            if similarity >= threshold:
                return True  # High match found

    return False  # No relevant match found

def prompt_model_check(query, topics_1, topics_2, model_name="mistralai/Mixtral-8x7B-Instruct-v0.1"):
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
            4. **Technology** are innovations from F1 teams to improve their vehicles.
            5. Your understanding of these aspects should guide your assessment. 
            6. For each word in the question, determine if it pertains to a driver, race, circuit, or technology. If a relevant term is identified, analyze it in relation to the associated topics.
            Evaluate whether the question relates to the following options:
            - **Option 1**: {topics_1} (Data source only from 2000 and onwards, discard if it includes any other year)
            - **Option 2**: {topics_2} (Data source only from 1950 and onwards, discard if it includes any other year)

            Please respond with:
            - "1" if the question relates to Option 1,
            - "2" if it relates to Option 2, or
            - "no" if neither applies.

            **Question**: "{query}"
            """
        }
    ]

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=5,
        stream=True
    )

    answer = ""
    for chunk in response:
        answer += chunk.choices[0].delta.content

    normalized_answer = answer.strip().lower()
    if "1" in normalized_answer:
        return 1  # Matches Option 1
    elif "2" in normalized_answer:
        return 2  # Matches Option 2
    else:
        return 0  # Matches neither

def routing_rag(query, topics):
    # Step 1: Check if the specific model is similar
    if is_specific_model_similar(query, topics):
        return 1

    # Step 2 and 3: Check if the query is related to specific topics
    topics_option_1 = [
        "General information on Formula 1 vehicles",
        "Vehicle technology and innovations for Formula 1",
        "Formula 1 car models"
    ]
    topics_option_2 = {
        "Drivers": ["Drivers participate in races.", "Drivers have standings based on their performance.", "Drivers win races in various years.", "Drivers have personal information (number, surname, code, forename, date of birth)."],
        "Races": ["Races are conducted on circuits.", "Races result in wins for drivers.", "Races have name and date."],
        "Circuits": ["Circuits host multiple races.", "Different circuits have different characteristics such as name and location."],
        "Standings": ["Each driver has a standing for a race.", "A race is won by a driver."]
    }

    # Call the model check function
    return prompt_model_check(query, topics_option_1, topics_option_2)

# Usage example (to be placed in another .py file):
if __name__ == "__main__":
    API_TOKEN = os.getenv("API_TOKEN")
    TOPICS_PATH = os.getenv("PROCESSED_DATA_PATH")

    initialize_inference_client(API_TOKEN)
    topics = load_topics(TOPICS_PATH)  # Load topics once at the beginning
    
    while True:
        # Ask the user for a question
        user_query = input("Please enter your question (or type 'exit' to quit): ")
        
        if user_query.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break  # Exit the loop if the user types 'exit'
        
        result = routing_rag(user_query, topics)  # Pass the loaded topics
        print(f"Result: {result}")  # Print the result without terminating the program