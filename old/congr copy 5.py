import os
import mimetypes
import hashlib
from datetime import datetime
from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD
from urllib.parse import quote

gist = Namespace("https://w3id.org/ontology/semanticarts/gist/")
congr = Namespace("https://ontologies.semanticarts.com/congr/")
congr3 = Namespace("https://data.semanticarts.com/congr/")

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
    g.bind('gist', gist)
    g.bind('congr', congr)
    g.bind('congr3', congr3)

    for root, dirs, files in os.walk(dir_path):
        dir_hash = location_hash(root + str(os.path.getmtime(root)))
        dir_node = URIRef(congr3 + "_Directory_" + quote(root, safe='') + "_" + dir_hash)
        g.add((dir_node, RDF.type, gist.Collection))
        g.add((dir_node, gist.name, Literal(os.path.basename(root), datatype=XSD.string)))
        g.add((dir_node, congr.pathString, Literal(root, datatype=XSD.string)))

        parent_dir_path = os.path.dirname(root)
        parent_dir_hash = location_hash(parent_dir_path + str(os.path.getmtime(parent_dir_path)))
        parent_dir_node = URIRef(congr3 + "_Directory_" + quote(parent_dir_path, safe='') + "_" + parent_dir_hash)
        if parent_dir_path != dir_path: 
            g.add((dir_node, gist.isMemberOf, parent_dir_node))

        for filename in files:
            file_path = os.path.join(root, filename)

            if os.path.isfile(file_path):
                file_location_hash = location_hash(file_path + str(os.path.getmtime(file_path)))
                file_node = URIRef(congr3 + "_Content_" + quote(filename, safe='') + "_" + file_location_hash)

                g.add((file_node, RDF.type, gist.Content))
                g.add((file_node, gist.name, Literal(filename, datatype=XSD.string)))
                
                # Add magnitude information for file size
                size_node = URIRef(congr3 + "_InformationQuantity_" + quote(filename, safe='') + "_" + file_location_hash)
                g.add((size_node, gist.hasUnitOfMeasure, XSD.byte))
                g.add((size_node, gist.hasValue, Literal(os.path.getsize(file_path), datatype=XSD.integer)))
                g.add((file_node, gist.hasMagnitude, size_node))

                g.add((file_node, congr.createDateTime, Literal(datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(), datatype=XSD.dateTime)))
                g.add((file_node, congr.modifyDateTime, Literal(datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(), datatype=XSD.dateTime)))

                mime_type = mimetypes.guess_type(file_path)[0]
                if mime_type:
                    mime_type_node = URIRef(gist + "_MediaType_" + quote(mime_type.replace('/', ''), safe=''))
                    g.add((mime_type_node, RDF.type, gist.MediaType))
                    g.add((file_node, congr.hasMediaType, mime_type_node))

                fingerprint = content_hash(file_path)
                g.add((file_node, congr.fingerprint, Literal(fingerprint, datatype=XSD.string)))

                g.add((file_node, gist.isMemberOf, dir_node))

    g.serialize(format='turtle', destination='output.ttl')

generate_file_metadata('C:\\Users\\StevenChalem\\congr-test')
