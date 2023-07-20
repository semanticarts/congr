import csv
from rdflib import Graph, Namespace

# Define the RDF graph and namespace
g = Graph()
congr = Namespace('https://ontologies.semanticarts.com/congr/')
gist = Namespace('https://w3id.org/ontology/semanticarts/gist/')

# Load the RDF graph
g.parse(r"C:\\Users\StevenChalem\\Semantic Arts\SA Staff - Documents\\InternalSystems\\.congr\\ClientsAndPartners7-20-23.ttl", format="turtle")

# Extract path strings and count files/subdirectories
location_dict = {}
for s, p, o in g.triples((None, congr.pathString, None)):
    path_string = str(o)
    file_count = len(list(g.triples((s, gist.hasLocation, None))))
    location_dict[path_string] = file_count

# Sort the dictionary by path strings
location_dict = dict(sorted(location_dict.items()))

# Write the path strings and counts to a CSV file
with open('ignore/output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Path", "Count"])  # Writing headers
    for path, count in location_dict.items():
        writer.writerow([path, count])
