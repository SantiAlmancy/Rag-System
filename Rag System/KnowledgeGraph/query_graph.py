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
        sparql = SPARQLWrapper("http://127.0.0.1:7200/repositories/F1A")
        sparql.setReturnFormat(JSON)
        return sparql

    def generateSPARQLQuery(self, question):
        """Generate SPARQL query from natural language question"""
        schema = f""" 
        1. Driver
        - URI Pattern: <http://example.org/f1/driver/[name]>
        - Properties:
            * f1:name (string)

        2. Race
        - URI Pattern: <http://example.org/f1/race/[id]>
        - Properties:
            * f1:year (integer)
            * schema1:name (string)

        3. Standing
        - URI Pattern: <http://example.org/f1/standing/[id]>
        - Properties:
            * f1:hasDriver → Driver
            * f1:hasRace → Race
            * f1:position (integer)"""
        
        query1 = f"""PREFIX f1: <http://example.org/f1/>
        PREFIX schema1: <http://schema.org/>

        SELECT DISTINCT ?name
        WHERE {{
            ?standing f1:hasDriver ?driver ;
                    f1:hasRace ?race .

            ?driver a f1:Driver ;
                    f1:name ?name .

            ?race f1:year 2020 .  # Specify the year
        }}
        """

        query2 = f"""PREFIX f1: <http://example.org/f1/>
        PREFIX schema1: <http://schema.org/>

        SELECT ?name ?position
        WHERE {{
            ?standing f1:hasDriver ?driver ;
                        f1:hasRace ?race ;
                        f1:position ?position .

            ?driver a f1:Driver ;
                    f1:name ?name .

            ?race f1:year 2020 .  # Specify the year of the race
            FILTER(?position = 1)
        }}
        """
        
        prompt = f"""

        * RDF SCHEMA *
        {schema}

        * TASK *
            I will provide you with a query in natural language. Your goal is to translate it to a SPARQL query
            following the previous ontology specifications (properties' names and classes' names).

        **CASES**:
        1. If the question is "What drivers raced in the [year]?", refer to this query:
        {query1}

        2. If the question is "In the [year] what drivers won?", refer to this query:
        {query2}
    
        * OUTPUT FORMAT REMINDER *
        Return only a valid SPARQL query (don't include any other text, nor special characters, the variables in the format ?variable must be well written) and the results 
        should only return what is asked in the question.

        QUERY FOR: "{question}" """


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
        
        if lines[0].startswith('QUERY:'):
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