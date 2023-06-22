import os
from datetime import datetime
from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD
from urllib.parse import quote
#import time
#import uuid

gist = Namespace("https://w3id.org/semanticarts/gist/")
ex = Namespace("http://example.org/files/") # Namespace for our file metadata

# Read file metadata from a directory and generate a turtle file
def generate_file_metadata(dir_path):
    # Create a graph
    g = Graph()
    g.bind('gist', gist) # Associate the prefix 'gist' with the gist namespace

    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)

        if os.path.isfile(file_path):
            # Create a node for the file
            # safe_filename = quote(filename, safe='')  # URL-safe encoding
            # file_node = URIRef(ex + safe_filename)
            file_node = URIRef(ex + quote(filename, safe=''))

            # Add triples to the graph
            g.add((file_node, RDF.type, gist.Content))
            g.add((file_node, ex.name, Literal(filename, datatype=XSD.string)))
            g.add((file_node, ex.size, Literal(os.path.getsize(file_path), datatype=XSD.integer)))
            g.add((file_node, ex.creation_time, Literal(datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(), datatype=XSD.dateTime)))
            g.add((file_node, ex.modification_time, Literal(datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(), datatype=XSD.dateTime)))
            g.add((file_node, ex.directory, Literal(os.path.dirname(file_path), datatype=XSD.string)))

    # Serialize the graph in turtle format
    g.serialize(format='turtle', destination='output.ttl')

generate_file_metadata('C:\\Users\\StevenChalem\\congr-test')
# generate_file_metadata('C:\\Users\\StevenChalem\\git')
