import os
import mimetypes
import hashlib
from datetime import datetime
from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD
from urllib.parse import quote

gist = Namespace("https://w3id.org/semanticarts/gist/")
dat = Namespace("https://data.semanticarts.com/congr/") # This is probably wrong

def location_hash(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()[:10]

def content_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()

def generate_file_metadata(dir_path):
    # Create a graph
    g = Graph()
    g.bind('gist', gist)  # Associate the prefix 'gist' with the gist namespace
    g.bind('dat', dat)  # Associate the prefix 'dat' with the dat namespace

    # Use os.walk() to traverse directory tree from dir_path downward, recording all files and directories
    for root, dirs, files in os.walk(dir_path):
        # Create a node for the directory
        dir_hash = location_hash(root + str(os.path.getmtime(root)))
        dir_node = URIRef(dat + "_Directory_" + quote(root, safe='') + "_" + dir_hash)
        g.add((dir_node, RDF.type, gist.Directory))
        g.add((dir_node, dat.name, Literal(os.path.basename(root), datatype=XSD.string)))
        g.add((dir_node, dat.path, Literal(root, datatype=XSD.string)))

        # Create a node for the parent directory
        parent_dir_path = os.path.dirname(root)
        parent_dir_hash = location_hash(parent_dir_path + str(os.path.getmtime(parent_dir_path)))
        parent_dir_node = URIRef(dat + "_Directory_" + quote(parent_dir_path, safe='') + "_" + parent_dir_hash)
        if parent_dir_path != dir_path:  # Exclude the root directory
            g.add((dir_node, gist.isMemberOf, parent_dir_node))

        for filename in files:
            file_path = os.path.join(root, filename)

            if os.path.isfile(file_path):
                # Create a node for the file
                file_location_hash = location_hash(file_path + str(os.path.getmtime(file_path)))
                file_node = URIRef(dat + "_Content_" + quote(filename, safe='') + "_" + file_location_hash)

                # Add triples to the graph for the file node and its properties
                g.add((file_node, RDF.type, gist.Content))
                g.add((file_node, dat.name, Literal(filename, datatype=XSD.string)))
                g.add((file_node, dat.size, Literal(os.path.getsize(file_path), datatype=XSD.integer)))
                g.add((file_node, dat.creation_time, Literal(datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(), datatype=XSD.dateTime)))
                g.add((file_node, dat.modification_time, Literal(datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(), datatype=XSD.dateTime)))
                g.add((file_node, dat.directory, Literal(os.path.dirname(file_path), datatype=XSD.string)))

                # Determine and add the MIME type
                mime_type = mimetypes.guess_type(file_path)[0]
                if mime_type:
                    g.add((file_node, dat.mime_type, Literal(mime_type, datatype=XSD.string)))

                # Add content hash for duplicate detection
                fingerprint = content_hash(file_path)
                g.add((file_node, dat.fingerprint, Literal(fingerprint, datatype=XSD.string)))

                # Add relationship between directory and file
                g.add((file_node, gist.isMemberOf, dir_node))

    # Serialize the graph in turtle format
    g.serialize(format='turtle', destination='output.ttl')

generate_file_metadata('C:\\Users\\StevenChalem\\congr-test')
