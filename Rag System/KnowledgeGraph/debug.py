# debug_graph.py
from rdflib import Graph, Namespace
from rdflib.namespace import FOAF
import os

# Load environment variables
load_dotenv()
G_path = os.getenv("GRAPH_PATH")

def debug_graph(file_path=G_path):
    g = Graph()
    g.parse(file_path, format="turtle")
    
    print("Total number of triples:", len(g))
    
    # Print all driver names in the graph
    print("\nAll driver names in the graph:")
    query = """
    PREFIX foaf: <http://www.w3.org/ns/foaf/0.1/>
    SELECT ?name
    WHERE {
        ?driver foaf:givenName ?name .
    }
    """
    
    for row in g.query(query):
        print(row.name)

if __name__ == "__main__":
    debug_graph()
