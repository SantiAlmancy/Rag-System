from huggingface_hub import InferenceClient
from SPARQLWrapper import SPARQLWrapper, JSON
from dotenv import load_dotenv
import os
import sys

class F1QuerySystem:
    def __init__(self):
        self.client = self._initializeModelAPI()
        self.sparql = self._initializeSPARQLWrapper()

    def _initializeModelAPI(self):
        """Initialize the Hugging Face client"""
        load_dotenv()
        apiToken = os.getenv("API_TOKEN")
        return InferenceClient(token=apiToken)

    def _initializeSPARQLWrapper(self):
        """Initialize the SPARQL wrapper for GraphDB"""
        sparql = SPARQLWrapper("http://127.0.0.1:7200/repositories/F1")
        sparql.setReturnFormat(JSON)
        return sparql

    def generateSPARQLQuery(self, question):
        """Generate SPARQL query from natural language question"""
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
Include only the SPARQL query in your response, with appropriate prefixes.

SPARQL Query:
"""
        try:
            response = self.client.text_generation(
                prompt,
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                max_new_tokens=500,
                temperature=0.1,
                stream=True
            )

            sparqlQuery = ""
            for chunk in response:
                sparqlQuery += chunk

            return sparqlQuery.strip()
        except Exception as e:
            raise Exception(f"Error generating SPARQL query: {str(e)}")

    def executeQuery(self, query):
        """Execute SPARQL query and return results"""
        try:
            self.sparql.setQuery(query)
            results = self.sparql.query().convert()
            return results
        except Exception as e:
            raise Exception(f"Error executing SPARQL query: {str(e)}")

    def processQuestion(self, question):
        """Process a natural language question and return results"""
        try:
            query = self.generateSPARQLQuery(question)
            print("\nGenerated SPARQL Query:")
            print(query)
            print("\nExecuting query...")
            
            results = self.executeQuery(query)
            return results
        except Exception as e:
            print(f"Error processing question: {str(e)}")
            return None

def query_f1_knowledge_graph(question):
    """Function to be called from outside with a question parameter"""
    try:
        querySystem = F1QuerySystem()
        results = querySystem.processQuestion(question)
        return results
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    # This block will only run if the script is run directly
    if len(sys.argv) > 1:
        # Get the question from command line arguments
        question = ' '.join(sys.argv[1:])
        results = query_f1_knowledge_graph(question)
        if results:
            print("\nResults:")
            print(results)
    else:
        print("No question provided. Please provide a question as an argument.")