from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

def initializeModelAPI():
    load_dotenv()
    apiToken = os.getenv("API_TOKEN")
    client = InferenceClient(token=apiToken)
    return client

def generateSPARQLQuery(client, question):
    # Define the prompt for the model
    prompt = f"""You are a SPARQL query generator for a Formula 1 knowledge graph. The graph has the following structure:

Circuits:
- URI pattern: <http://example.org/f1/circuit/[name]>
- Properties: schema1:country, schema1:latitude, schema1:longitude, schema1:location, schema1:name

Races:
- URI pattern: <http://example.org/f1/race/[id]>
- Properties: f1:hasCircuit, f1:round, f1:year, schema1:date, schema1:name

Drivers:
- URI pattern: <http://example.org/f1/driver/[name]>
- Properties: f1:code, f1:number, schema1:birthDate, schema1:nationality, foaf:familyName, foaf:givenName

Standings:
- URI pattern: <http://example.org/f1/standing/[id]>
- Properties: f1:hasDriver, f1:hasRace, f1:points, f1:position, f1:wins

Given this question: "{question}"
Generate a SPARQL query that would answer this question using the knowledge graph structure above.
Use appropriate prefixes and provide only the SPARQL query as output.

SPARQL Query:
"""

    # Get response from the model using text-generation
    response = client.text_generation(
        prompt,
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        max_new_tokens=500,
        temperature=0.1,
        stream=True
    )

    # Accumulate the response
    sparqlQuery = ""
    for chunk in response:
        sparqlQuery += chunk

    return sparqlQuery.strip()

def formatSPARQLQuery(query):
    """Format the SPARQL query with proper indentation and line breaks"""
    # Add common prefixes
    prefixes = """PREFIX f1: <http://example.org/f1/>
PREFIX schema1: <http://schema.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

"""
    return query

def main():
    client = initializeModelAPI()
    
    # Example questions to test
    question = [
        "Which drivers won races in 1967?"
    ]
    
# Test with a specific question or loop through examples
    print(f"\nQuestion: {question}")
    try:
        sparql_query = generateSPARQLQuery(client, question)
        formatted_query = formatSPARQLQuery(sparql_query)
        print("\nGenerated SPARQL Query:")
        print(formatted_query)
    except Exception as e:
        print(f"Error generating query: {str(e)}")
    print("-" * 80)

if __name__ == "__main__":
    main()