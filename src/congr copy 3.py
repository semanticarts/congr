import os
from datetime import datetime
import hashlib
from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD
from urllib.parse import quote
import mimetypes

gist = Namespace("https://w3id.org/semanticarts/gist/")
dat = Namespace("http://data.semanticarts.com/congr/") # Namespace for our file metadata

# Create a function to generate a SHA256 hash
def generate_hash(input_string, length=None):
    hash_result = hashlib.sha256(input_string.encode()).hexdigest()
    if length is not None:
        return hash_result[:length]
    else:
        return hash_result

def generate_file_metadata(dir_path):
    # Create a graph
    g = Graph()
    g.bind('gist', gist)  # Associate the prefix 'gist' with the gist namespace
    g.bind('dat', dat)  # Associate the prefix 'dat' with the dat namespace

    # Use os.walk() to traverse entire directory tree and identify directories and files
    for root, dirs, files in os.walk(dir_path):
        # Generate a hash for the directory IRI
        dir_hash = generate_hash(root + str(os.path.getctime(root)), length=10)
        # Create a node for the directory using the new format
        dir_node = URIRef(dat + "_Directory_" + quote(os.path.basename(root), safe='') + "_" + dir_hash)
        
        g.add((dir_node, RDF.type, gist.Container))
        g.add((dir_node, dat.name, Literal(os.path.basename(root), datatype=XSD.string)))
        g.add((dir_node, dat.path, Literal(root, datatype=XSD.string)))

        # Create a node for the parent directory
        parent_dir_path = os.path.dirname(root)
        parent_dir_hash = generate_hash(parent_dir_path + str(os.path.getctime(parent_dir_path)), length=10)
        parent_dir_node = URIRef(dat + "_Directory_" + quote(os.path.basename(parent_dir_path), safe='') + "_" + parent_dir_hash)
        if parent_dir_path != dir_path:  # Exclude the root directory
            g.add((dir_node, gist.isMemberOf, parent_dir_node))

        for filename in files:
            file_path = os.path.join(root, filename)

            if os.path.isfile(file_path):
                # Generate a short hash for the IRI and a longer one for the property
                short_hash = generate_hash(file_path + str(os.path.getmtime(file_path)), length=10)
                long_hash = generate_hash(file_path + str(os.path.getmtime(file_path)))
                # Create a node for the file using the new format, with underscore between file name and hash
                file_node = URIRef(dat + "_Content_" + quote(filename, safe='') + "_" + short_hash)

                # Add triples for the file node and its properties
                g.add((file_node, RDF.type, gist.Content))
                g.add((file_node, dat.name, Literal(filename, datatype=XSD.string)))
                g.add((file_node, dat.size, Literal(os.path.getsize(file_path), datatype=XSD.integer)))
                g.add((file_node, dat.creation_time, Literal(datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(), datatype=XSD.dateTime)))
                g.add((file_node, dat.modification_time, Literal(datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(), datatype=XSD.dateTime)))
                g.add((file_node, dat.directory, Literal(os.path.dirname(file_path), datatype=XSD.string)))
                g.add((file_node, dat.fingerprint, Literal(long_hash, datatype=XSD.string)))  # Use 'fingerprint' instead of 'hash'

                # Determine and add the MIME type
                mime_type = mimetypes.guess_type(file_path)[0]
                if mime_type:
                    g.add((file_node, dat.mime_type, Literal(mime_type, datatype=XSD.string)))

                # Add relationship between directory and file
                g.add((file_node, gist.isMemberOf, dir_node))

    # Serialize the graph in turtle format
    g.serialize(format='turtle', destination='output3.ttl')

generate_file_metadata('C:\\Users\\StevenChalem\\congr-test')
