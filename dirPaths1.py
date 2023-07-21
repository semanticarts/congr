import csv
from rdflib import Graph, Namespace

# Define the RDF graph and namespace
g = Graph()
congr = Namespace('https://ontologies.semanticarts.com/congr/')
gist = Namespace('https://w3id.org/ontology/semanticarts/gist/')

# Load the RDF graph
g.parse(r"C:\\Users\StevenChalem\\Semantic Arts\SA Staff - Documents\\InternalSystems\\.congr\\MarketingAndSales7-20-23.ttl", format="turtle")

# Extract path strings and count files/subdirectories
location_dict = {}
dir_count = 0
file_count = 0
for s, p, o in g.triples((None, congr.pathString, None)):
    path_string = str(o)
    file_cnt = len(list(g.triples((s, gist.hasLocation, None))))
    location_dict[path_string] = file_cnt
    dir_count += 1
    file_count += file_cnt

    # Print directory and file counts every 1000 directories
    if dir_count % 1000 == 0:
        print(f'Directories processed: {dir_count}, Files processed: {file_count}')

# Sort the dictionary by path strings
location_dict = dict(sorted(location_dict.items()))

# Write the path strings and counts to a CSV file
with open('ignore/output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Path", "Count"])  # Writing headers
    for path, count in location_dict.items():
        writer.writerow([path, count])
