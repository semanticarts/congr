import os
from datetime import datetime
from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD
from urllib.parse import quote
import mimetypes
#import time
#import uuid

gist = Namespace("https://w3id.org/semanticarts/gist/")
ex = Namespace("http://example.org/files/") # Namespace for our file metadata

def generate_file_metadata(dir_path):
    # Create a graph
    g = Graph()
    g.bind('gist', gist)  # Associate the prefix 'gist' with the gist namespace

    # Use os.walk() to cover subdirectories as well
    for root, dirs, files in os.walk(dir_path):
        # Create a node for the directory
        dir_node = URIRef(ex + quote(root, safe=''))
        g.add((dir_node, RDF.type, gist.Container))
        g.add((dir_node, ex.name, Literal(os.path.basename(root), datatype=XSD.string)))
        g.add((dir_node, ex.path, Literal(root, datatype=XSD.string)))

        # Create a node for the parent directory
        parent_dir_path = os.path.dirname(root)
        parent_dir_node = URIRef(ex + quote(parent_dir_path, safe=''))
        if parent_dir_path != dir_path:  # Exclude the root directory
            g.add((dir_node, gist.isMemberOf, parent_dir_node))

        for filename in files:
            file_path = os.path.join(root, filename)

            if os.path.isfile(file_path):
                # Create a node for the file
                file_node = URIRef(ex + quote(filename, safe=''))

                # Add triples to the graph
                g.add((file_node, RDF.type, gist.Content))
                g.add((file_node, ex.name, Literal(filename, datatype=XSD.string)))
                g.add((file_node, ex.size, Literal(os.path.getsize(file_path), datatype=XSD.integer)))
                g.add((file_node, ex.creation_time, Literal(datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(), datatype=XSD.dateTime)))
                g.add((file_node, ex.modification_time, Literal(datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(), datatype=XSD.dateTime)))
                g.add((file_node, ex.directory, Literal(os.path.dirname(file_path), datatype=XSD.string)))

                # Determine and add the MIME type
                mime_type = mimetypes.guess_type(file_path)[0]
                if mime_type:
                    g.add((file_node, ex.mime_type, Literal(mime_type, datatype=XSD.string)))

                # Add relationship between directory and file
                g.add((file_node, gist.isMemberOf, dir_node))

    # Serialize the graph in turtle format
    g.serialize(format='turtle', destination='output.ttl')

generate_file_metadata('C:\\Users\\StevenChalem\\congr-test')
