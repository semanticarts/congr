import spacy

# Load a pre-trained spaCy model
nlp = spacy.load('en_core_web_sm')

# Let's say these are your unique directory names
unique_directory_names = ['Microsoft', 'JohnDoe', 'iPhone', 'Google', 'Smith']

# For each directory name, predict its entity type using the spaCy model
for directory_name in unique_directory_names:
    doc = nlp(directory_name)
    for entity in doc.ents:
        print(f'{directory_name}: {entity.label_}')
