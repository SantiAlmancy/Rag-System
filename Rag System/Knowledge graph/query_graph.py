# query_graph.py
from rdflib import Graph, Namespace
from rdflib.namespace import FOAF, XSD

G_path = r"C:\Users\Ale\UPB\8vo Semestre\Topicos IA\Rag-System\Rag System\Knowledge graph\knowledge_graphs\f1_graph.ttl"

class F1KnowledgeGraph:
    def __init__(self, graph_path=G_path):
        # Create namespaces
        self.F1 = Namespace("http://example.org/f1/")
        self.SCHEMA = Namespace("http://schema.org/")
        
        # Load the graph
        self.g = Graph()
        self.g.parse(graph_path, format="turtle")
        
        # Bind namespaces
        self.g.bind("f1", self.F1)
        self.g.bind("schema", self.SCHEMA)
        self.g.bind("foaf", FOAF)

    def query_driver_info(self, driver_ref):
        driver_uri = f"<http://example.org/f1/driver/{driver_ref}>"
        print(f"Querying driver URI: {driver_uri}")
        
        query = f"""
        PREFIX f1: <http://example.org/f1/>
        PREFIX schema: <http://schema.org/>
        PREFIX foaf: <http://www.w3.org/ns/foaf/0.1/>
        
        SELECT ?givenName ?familyName ?nationality ?birthDate
        WHERE {{
            {driver_uri} foaf:givenName ?givenName ;
                        foaf:familyName ?familyName ;
                        schema:nationality ?nationality ;
                        schema:birthDate ?birthDate .
        }}
        """
        print("Running driver info query...")
        print(query)  # Print the query before executing it
        results = self.g.query(query)
        print(f"Number of results: {len(results)}")  # Check how many results were returned
        return results

    def query_driver_wins_by_year(self, year):
        query = """
        PREFIX f1: <http://example.org/f1/>
        PREFIX foaf: <http://www.w3.org/ns/foaf/0.1/>
        
        SELECT ?givenName ?familyName (SUM(?wins) as ?totalWins)
        WHERE {
            ?standing f1:hasDriver ?driver ;
                     f1:wins ?wins ;
                     f1:hasRace ?race .
            ?race f1:year ?year .
            ?driver foaf:givenName ?givenName ;
                    foaf:familyName ?familyName .
            FILTER(?year = %d)
        }
        GROUP BY ?givenName ?familyName
        ORDER BY DESC(?totalWins)
        """
        
        return self.g.query(query % year)

    def query_circuits_by_country(self, country):
        query = """
        PREFIX f1: <http://example.org/f1/>
        PREFIX schema: <http://schema.org/>
        
        SELECT ?name ?location ?lat ?lng
        WHERE {
            ?circuit a f1:Circuit ;
                    schema:name ?name ;
                    schema:location ?location ;
                    schema:latitude ?lat ;
                    schema:longitude ?lng ;
                    schema:country ?countryName .
            FILTER(?countryName = "%s")
        }
        """
        
        return self.g.query(query % country)

    def query_all_drivers(self):
        query = """
        PREFIX f1: <http://example.org/f1/>
        PREFIX foaf: <http://www.w3.org/ns/foaf/0.1/>
        PREFIX schema: <http://schema.org/>
        
        SELECT ?givenName ?familyName ?nationality
        WHERE {
            ?driver a f1:Driver ;
                    foaf:givenName ?givenName ;
                    foaf:familyName ?familyName ;
                    schema:nationality ?nationality .
        }
        ORDER BY ?familyName ?givenName
        """
        
        return self.g.query(query)

# Example usage
if __name__ == "__main__":
    try:
        # Create instance of F1KnowledgeGraph
        kg = F1KnowledgeGraph()
        
        # Example queries
        print("Driver Information for Hamilton:")
        results = kg.query_driver_info("hamilton")
        for row in results:
            print(f"Name: {row.givenName} {row.familyName}")
            print(f"Nationality: {row.nationality}")
            print(f"Birth Date: {row.birthDate}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")