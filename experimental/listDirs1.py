import csv
import os
import re
import spacy

from rdflib import Graph, Namespace

# Load Spacy language model
nlp = spacy.load("en_core_web_sm")

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

# Open first CSV file to write directory data with named entities
with open('directories.csv', 'w', newline='', encoding='utf-8') as f1:
    writer1 = csv.DictWriter(f1, fieldnames=['IRI', 'Path', 'Name', 'Entities'])
    writer1.writeheader()

    # Open second CSV file to write unique directory names
    with open('unique_directory_names.csv', 'w', newline='', encoding='utf-8') as f2:
        writer2 = csv.writer(f2)
        writer2.writerow(['Name'])

        unique_names = set()
        for row in qres:
            path_string = str(row[1])
            directory_names = re.split(r'[\s_/\\]+', path_string)

            # Update unique names set
            unique_names.update(directory_names)

            # Get named entities using Spacy
            named_entities = []
            for name in directory_names:
                doc = nlp(name)
                named_entities.extend([ent.text for ent in doc.ents])

            # Write to directories.csv
            writer1.writerow({'IRI': str(row[0]), 'Path': str(row[1]), 'Name': str(row[2]), 'Entities': named_entities})

        # Write unique names to unique_directory_names.csv
        for name in unique_names:
            writer2.writerow([name])
