# debug_graph.py
from rdflib import Graph, Namespace
from rdflib.namespace import FOAF


G_path = r"C:\Users\Ale\UPB\8vo Semestre\Topicos IA\Rag-System\Rag System\Knowledge graph\knowledge_graphs\f1_graph.ttl"
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