import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the CSV files
drivers = pd.read_csv(r'C:\Users\Ale\UPB\8vo Semestre\Topicos IA\Rag-System\Rag System\Knowledge graph\drivers.csv')
driver_standings = pd.read_csv(r'C:\Users\Ale\UPB\8vo Semestre\Topicos IA\Rag-System\Rag System\Knowledge graph\driver_standings.csv')
circuits = pd.read_csv(r'C:\Users\Ale\UPB\8vo Semestre\Topicos IA\Rag-System\Rag System\Knowledge graph\circuits.csv')
races = pd.read_csv(r'C:\Users\Ale\UPB\8vo Semestre\Topicos IA\Rag-System\Rag System\Knowledge graph\races.csv')

# Create the knowledge graph
G = nx.Graph()

# Add nodes
for _, row in drivers.iterrows():
    G.add_node(row['driverRef'], label=f"{row['forename']} {row['surname']}", type='driver')

for _, row in circuits.iterrows():
    G.add_node(row['circuitRef'], label=row['name'], type='circuit')

for _, row in races.iterrows():
    G.add_node(f"race_{row['raceId']}", label=row['name'], type='race')

# Add edges
for _, row in driver_standings.iterrows():
    driver_ref = drivers.loc[drivers['driverId'] == row['driverId']]['driverRef'].values[0]
    G.add_edge(driver_ref, f"race_{row['raceId']}", label=row['position'])

for _, row in races.iterrows():
    circuit_ref = circuits.loc[circuits['circuitId'] == row['circuitId']]['circuitRef'].values[0]
    G.add_edge(f"race_{row['raceId']}", circuit_ref, label=row['name'])

for _, row in drivers.iterrows():
    G.add_edge(row['driverRef'], row['nationality'], label='nationality')
    G.add_edge(row['driverRef'], row['dob'], label='date of birth')
    G.add_edge(row['driverRef'], row['number'], label='number')
    G.add_edge(row['driverRef'], row['code'], label='code')

# Visualize the knowledge graph
pos = nx.spring_layout(G)
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', font_size=8)
plt.show()