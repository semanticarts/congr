import csv
import os
import re
from rdflib import Graph, Namespace

def parse_directory_name(directory_name):
    # Use regular expression to identify CamelCased words and multiple delimiters
    parsed = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', directory_name))
    parsed = re.split(r'[\s_-]+', parsed)
    return [word for word in parsed if word]

# Load ttl file into a rdflib Graph
g = Graph()
g.parse(r"C:\Users\StevenChalem\Semantic Arts\SA Staff - Documents\InternalSystems\.congr\SharedFolders_MarketingAndSales_2023-07-19.ttl", format="turtle")

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

# To hold unique directory names
unique_names = set()

# Write the directories to a CSV file
with open('ignore/directories.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['IRI', 'Path', 'Name'])
    writer.writeheader()
    for row in qres:
        directory_name = str(row[2])
        parsed_name = parse_directory_name(directory_name)
        unique_names.update(parsed_name)
        writer.writerow({'IRI': str(row[0]), 'Path': str(row[1]), 'Name': ' '.join(parsed_name)})

# Write the unique directory names to a CSV file
with open('ignore/unique_directories.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for name in unique_names:
        writer.writerow([name])
