import csv
from rdflib import Graph, Namespace

# Load ttl file into a rdflib Graph
g = Graph()
g.parse("output/congr-output.ttl", format="turtle")

# Define data namespace
congr3 = Namespace('https://data.semanticarts.com/congr/')

# Query all subjects of type gist:Location, their pathString property and name property
qres = g.query(
    """
    PREFIX congr: <https://ontologies.semanticarts.com/congr/>
    PREFIX gist: <https://w3id.org/ontology/semanticarts/gist/>
    SELECT ?subject ?path ?name
    WHERE {
        ?subject a gist:Location ;
                 congr:pathString ?path ;
                 gist:name ?name .
    }
    """
)

# Create a set to store unique directory names
unique_dir_names = set()

# Write the query results directly to a CSV file
with open('output/directories.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['IRI', 'Path', 'Name'])
    writer.writeheader()
    for row in qres:
        writer.writerow({'IRI': str(row[0]), 'Path': str(row[1]), 'Name': str(row[2])})
        unique_dir_names.add(str(row[2]))

# Write the unique directory names to a second CSV file
with open('output/unique_directories.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for name in unique_dir_names:
        writer.writerow([name])
