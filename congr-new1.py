import os
import mimetypes
import hashlib
from datetime import datetime
from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD
from urllib.parse import quote
import argparse

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

def generate_file_metadata(dir_path, include_files=False, create_fingerprints=False, output_file='congr-output.ttl'):
    # Create a graph
    g = Graph()
    g.bind('gist', gist)
    g.bind('congr', congr)
    g.bind('congr3', congr3)

    root_dir_name = os.path.basename(os.path.abspath(dir_path))
    
    for root, dirs, files in os.walk(dir_path):
        if root == dir_path:
            dir_name = root_dir_name
        else:
            dir_name = os.path.basename(root)

        dir_hash = location_hash(dir_name + str(os.path.getmtime(root)))
        dir_node = URIRef(congr3 + "_Directory_" + quote(dir_name, safe='') + "_" + dir_hash)
        g.add((dir_node, RDF.type, gist.Collection))
        g.add((dir_node, gist.name, Literal(dir_name, datatype=XSD.string)))
        g.add((dir_node, congr.pathString, Literal(root.replace("\\", "/").replace("//", "/"), datatype=XSD.anyURI)))

        if root != dir_path:
            parent_dir_name = os.path.basename(os.path.dirname(root))
            parent_dir_hash = location_hash(parent_dir_name + str(os.path.getmtime(os.path.dirname(root))))
            parent_dir_node = URIRef(congr3 + "_Directory_" + quote(parent_dir_name, safe='') + "_" + parent_dir_hash)
            g.add((dir_node, gist.isMemberOf, parent_dir_node))

        for filename in files:
            file_path = os.path.join(root, filename)

            if os.path.isfile(file_path) and include_files:
                file_location_hash = location_hash(filename + str(os.path.getmtime(file_path)))
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

                if create_fingerprints:
                    fingerprint = content_hash(file_path)
                    g.add((file_node, congr.fingerprint, Literal(fingerprint, datatype=XSD.string)))

                g.add((file_node, gist.isMemberOf, dir_node))

    g.serialize(format='turtle', destination=output_file)

def main():
    parser = argparse.ArgumentParser(description='Generate file metadata.')
    parser.add_argument('dir_path', type=str, nargs='?', default=os.getcwd(), help='Path to the starting directory (default: current directory)')
    parser.add_argument('--files', dest='include_files', action='store_true', help='Include files in metadata')
    parser.add_argument('--no-files', dest='include_files', action='store_false', help='Exclude files from metadata')
    parser.set_defaults(include_files=False)

    parser.add_argument('--fingerprints', dest='create_fingerprints', action='store_true', help='Create file fingerprints')
    parser.add_argument('--no-fingerprints', dest='create_fingerprints', action='store_false', help='Exclude file fingerprints')
    parser.set_defaults(create_fingerprints=False)

    parser.add_argument('-o', '--output', dest='output_file', type=str, default='congr-output.ttl', help='Output file name (default: congr-output.ttl)')

    args = parser.parse_args()
    generate_file_metadata(args.dir_path, include_files=args.include_files, create_fingerprints=args.create_fingerprints, output_file=args.output_file)

if __name__ == '__main__':
    main()
