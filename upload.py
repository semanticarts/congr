# Upload a turtle file to triple store
# Shawn Goodwin, Steven Chalem, Semantic Arts 2023-07
from dotenv import dotenv_values
import requests
import sys
import urllib.parse

config = dotenv_values(".env")

def upload_triples(triple_file, named_graph):
    url = config["TRIPLESTORE_URL"] + "/statements"
    context = "<" + named_graph + ">"
    headers = {'Content-Type': 'text/turtle'}
    params = {"context": context}  # named graph URI
    
    with open(triple_file, 'rb') as f:
        data = f.read()
        response = requests.post(
            url,
            headers=headers,
            data=data,
            auth=(config["USERNAME"], config["PASSWORD"]),
            timeout=600,
            params=params)
    
    print(response.text)
        
def main():
    upload_triples(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()


