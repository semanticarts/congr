import os
import mimetypes
import hashlib
from datetime import datetime
from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD
from urllib.parse import quote
import argparse

SPACETIME_HASH_TRUNC_LENGTH = 10
CONTENT_HASH_CHUNK_SIZE = 4096

gist = Namespace("https://w3id.org/ontology/semanticarts/gist/")
congr = Namespace("https://ontologies.semanticarts.com/congr/")
congr3 = Namespace("https://data.semanticarts.com/congr/")

def spacetime_hash(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()[:SPACETIME_HASH_TRUNC_LENGTH]

def content_hash(file_path):
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as afile:
            for chunk in iter(lambda: afile.read(CONTENT_HASH_CHUNK_SIZE), b''):
                hasher.update(chunk)
    except IOError as e:
        print(f"Couldn't read {file_path}: {e}")
        return None
    return hasher.hexdigest()

def generate_file_metadata(starting_dir_path, include_files, create_fingerprints, output_file='congr-output.ttl'):
    g = Graph()
    g.bind('gist', gist)
    g.bind('congr', congr)
    g.bind('congr3', congr3)

    starting_dir_hash = spacetime_hash(starting_dir_path + str(os.path.getmtime(starting_dir_path)))
    starting_dir_node = URIRef(congr3 + "_Directory_" + quote(os.path.basename(starting_dir_path), safe='') + "_" + starting_dir_hash)
    g.add((starting_dir_node, RDF.type, gist.Collection))
    g.add((starting_dir_node, gist.name, Literal(os.path.basename(starting_dir_path), datatype=XSD.string)))
    g.add((starting_dir_node, congr.pathString, Literal(starting_dir_path, datatype=XSD.anyURI)))

    for root, dirs, files in os.walk(starting_dir_path):
        dir_hash = spacetime_hash(root + str(os.path.getmtime(root)))
        dir_node = URIRef(congr3 + "_Directory_" + quote(os.path.basename(root), safe='') + "_" + dir_hash)

        if root != starting_dir_path:
            g.add((dir_node, RDF.type, gist.Collection))
            g.add((dir_node, gist.name, Literal(os.path.basename(root), datatype=XSD.string)))
            g.add((dir_node, congr.pathString, Literal(root, datatype=XSD.anyURI)))
            g.add((dir_node, gist.isMemberOf, starting_dir_node))

        for filename in files:
            file_path = os.path.join(root, filename)
            
            if os.path.isfile(file_path) and include_files:
                file_location_hash = spacetime_hash(file_path + str(os.path.getctime(file_path)))
                file_node = URIRef(congr3 + "_Content_" + quote(filename, safe='') + "_" + file_location_hash)

                g.add((file_node, RDF.type, gist.Content))
                g.add((file_node, gist.name, Literal(filename, datatype=XSD.string)))

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
                    g.add((file_node, gist.hasMediaType, mime_type_node))

                if create_fingerprints:
                    fingerprint = content_hash(file_path)
                    g.add((file_node, congr.fingerprint, Literal(fingerprint, datatype=XSD.string)))

                g.add((file_node, gist.isMemberOf, dir_node))

    g.serialize(format='turtle', destination=output_file)

def main():
    parser = argparse.ArgumentParser(description='Triplify filestore metadata.')
    parser.add_argument('starting_dir_path', type=str, nargs='?', default='C:/Users/StevenChalem/congr-test', help='Path to the starting directory.')

    parser.add_argument('--files', dest='include_files', action='store_true', help='Include files in metadata')
    parser.add_argument('--no-files', dest='include_files', action='store_false', help='Exclude files from metadata')
    parser.set_defaults(include_files=True)

    parser.add_argument('--fingerprints', dest='create_fingerprints', action='store_true', help='Create file fingerprints')
    parser.add_argument('--no-fingerprints', dest='create_fingerprints', action='store_false', help='Exclude file fingerprints')
    parser.set_defaults(create_fingerprints=True)

    parser.add_argument('-o', '--output', dest='output_file', type=str, default='output/congr-output.ttl', help='Output file name (default: congr-output.ttl)')

    args = parser.parse_args()
    generate_file_metadata(args.starting_dir_path, include_files=args.include_files, create_fingerprints=args.create_fingerprints, output_file=args.output_file)

if __name__ == '__main__':
    main()
