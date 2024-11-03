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
        prompt = f"""You are a specialized SPARQL query generator for a Formula 1 knowledge graph. Your task is to generate ONLY a valid SPARQL query, without any additional text or explanations.

        KNOWLEDGE GRAPH STRUCTURE:
        1. Driver Entity:
        - URI: <http://example.org/f1/driver/[name]>
        - Required Properties:
            * foaf:givenName (string)
            * foaf:familyName (string)

        2. Race Entity:
        - URI: <http://example.org/f1/race/[id]>
        - Required Properties:
            * f1:year (integer)
            * schema1:name (string)
        - Note: [id] is independent of the race year

        3. Standing Entity:
        - URI: <http://example.org/f1/standing/[id]>
        - Required Properties:
            * f1:hasDriver (links to Driver URI)
            * f1:hasRace (links to Race URI)
            * f1:points (decimal)
            * f1:position (integer)

        IMPORTANT RULES:
        1. Always include these prefixes:
        PREFIX f1: <http://example.org/f1/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX schema1: <http://schema.org/>
        2. Use correct property paths (e.g., ?standing f1:hasDriver ?driver)
        3. Match variable names with their content (e.g., ?givenName for foaf:givenName)
        4. Include necessary FILTER clauses for numerical comparisons
        5. Use proper nesting for complex queries
        6. Return only the SPARQL query, no explanations

        REFERENCE QUERY EXAMPLE:
        PREFIX f1: <http://example.org/f1/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX schema1: <http://schema.org/>

        SELECT ?givenName ?familyName ?position
        WHERE {{
        ?standing f1:hasRace ?race ;
                    f1:hasDriver ?driver ;
                    f1:position ?position .
        ?race f1:year 2024 .
        ?driver foaf:givenName ?givenName ;
                foaf:familyName ?familyName .
        FILTER(?position <= 3)
        }}

        QUESTION TO ANSWER: "{question}"

        SPARQL Query:"""
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
            query = self.clean_sparql_response(query)
            print("\nCleaned Query:")
            print(query)
            print("\nExecuting query...")
            
            results = self.executeQuery(query)
            return results
        except Exception as e:
            print(f"Error processing question: {str(e)}")
            return None
    def clean_sparql_response(self, sparql_string):
        """Remove markdown code block markers and GPT end tokens from SPARQL query"""
        # Split the string into lines
        lines = sparql_string.split('\n')
        
        # Remove first line if it's a code block marker
        if lines[0].startswith('```'):
            lines = lines[1:]
        
        # Remove last line if it's a code block marker or GPT end token
        if lines[-1].strip().endswith('</s>'):
            lines[-1] = lines[-1].replace('</s>', '').strip()

        if lines[-1].startswith('```'):
            lines = lines[:-1]
        
        # Join the lines back together
        return '\n'.join(lines)

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