import os
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD

# Create namespaces for our data
F1 = Namespace("http://example.org/f1/")
SCHEMA = Namespace("http://schema.org/")

def create_rdf_graph():
    # Load the CSV files
    drivers = pd.read_csv(r'C:\Users\Ale\UPB\8vo Semestre\Topicos IA\Rag-System\Rag System\Knowledge graph\drivers.csv')
    driver_standings = pd.read_csv(r'C:\Users\Ale\UPB\8vo Semestre\Topicos IA\Rag-System\Rag System\Knowledge graph\driver_standings.csv')
    circuits = pd.read_csv(r'C:\Users\Ale\UPB\8vo Semestre\Topicos IA\Rag-System\Rag System\Knowledge graph\circuits.csv')
    races = pd.read_csv(r'C:\Users\Ale\UPB\8vo Semestre\Topicos IA\Rag-System\Rag System\Knowledge graph\races.csv')

    # Create RDF graph
    g = Graph()
    
    # Bind namespaces
    g.bind("f1", F1)
    g.bind("schema", SCHEMA)
    g.bind("foaf", FOAF)

    # Add drivers
    for _, row in drivers.iterrows():
        driver_uri = F1[f"driver/{row['driverRef']}"]
        g.add((driver_uri, RDF.type, F1.Driver))
        g.add((driver_uri, FOAF.givenName, Literal(row['forename'])))
        g.add((driver_uri, FOAF.familyName, Literal(row['surname'])))
        g.add((driver_uri, SCHEMA.nationality, Literal(row['nationality'])))
        g.add((driver_uri, SCHEMA.birthDate, Literal(row['dob'], datatype=XSD.date)))
        if pd.notna(row['number']):
            g.add((driver_uri, F1.number, Literal(row['number'])))
        if pd.notna(row['code']):
            g.add((driver_uri, F1.code, Literal(row['code'])))

    # Add circuits
    for _, row in circuits.iterrows():
        circuit_uri = F1[f"circuit/{row['circuitRef']}"]
        g.add((circuit_uri, RDF.type, F1.Circuit))
        g.add((circuit_uri, SCHEMA.name, Literal(row['name'])))
        g.add((circuit_uri, SCHEMA.location, Literal(row['location'])))
        g.add((circuit_uri, SCHEMA.country, Literal(row['country'])))
        g.add((circuit_uri, SCHEMA.latitude, Literal(row['lat'])))
        g.add((circuit_uri, SCHEMA.longitude, Literal(row['lng'])))

    # Add races
    for _, row in races.iterrows():
        race_uri = F1[f"race/{row['raceId']}"]
        g.add((race_uri, RDF.type, F1.Race))
        g.add((race_uri, SCHEMA.name, Literal(row['name'])))
        g.add((race_uri, SCHEMA.date, Literal(row['date'], datatype=XSD.date)))
        g.add((race_uri, F1.year, Literal(row['year'])))
        g.add((race_uri, F1.round, Literal(row['round'])))
        
        # Link race to circuit
        circuit_uri = F1[f"circuit/{circuits.loc[circuits['circuitId'] == row['circuitId'], 'circuitRef'].values[0]}"]
        g.add((race_uri, F1.hasCircuit, circuit_uri))

    # Add driver standings
    for _, row in driver_standings.iterrows():
        standing_uri = F1[f"standing/{row['driverStandingsId']}"]
        g.add((standing_uri, RDF.type, F1.Standing))
        
        driver_ref = drivers.loc[drivers['driverId'] == row['driverId'], 'driverRef'].values[0]
        driver_uri = F1[f"driver/{driver_ref}"]
        race_uri = F1[f"race/{row['raceId']}"]
        
        g.add((standing_uri, F1.hasDriver, driver_uri))
        g.add((standing_uri, F1.hasRace, race_uri))
        g.add((standing_uri, F1.points, Literal(row['points'])))
        g.add((standing_uri, F1.position, Literal(row['position'])))
        g.add((standing_uri, F1.wins, Literal(row['wins'])))

    return g

if __name__ == "__main__":
    # Create the graph
    g = create_rdf_graph()

    # Ensure the directory exists
    output_dir = os.path.join(os.path.dirname(__file__), 'knowledge_graphs')
    os.makedirs(output_dir, exist_ok=True)

    # Save the graph in different formats
    g.serialize(destination=os.path.join(output_dir, "f1_graph.ttl"), format="turtle")  # Turtle format (readable)
    g.serialize(destination=os.path.join(output_dir, "f1_graph.nt"), format="nt")      # N-Triples format
    g.serialize(destination=os.path.join(output_dir, "f1_graph.xml"), format="xml")    # RDF/XML format
    
    print("Graph has been saved successfully!")
