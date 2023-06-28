Content Grapher (congr)
=====

![conger on a file cabinet](./media/conger-on-a-file-cabinet-210x210.png)

Traverse a directory tree and write metadata to a turtle file. Optionally include file metadata and file fingerprints.

Usage
-----

`python congr.py [dir_path] [--files] [--no-files] [--fingerprints] [--no-fingerprints] [-o output_file]`

The options are:

`dir_path`: Specifies the starting directory for generating file metadata. If not provided, the current directory is used as the default starting directory.

`--files`: Includes files in the generated metadata.

`--no-files`: Excludes files from the generated metadata.

`--fingerprints`: Creates fingerprints for files in the generated metadata.

`--no-fingerprints`: Excludes file fingerprints from the generated metadata.

`-o output_file`: Specifies the name of the output file. If not provided, the default output file is ./output/congr-output.ttl.

Option defaults are changing frequently during development. Be explicit!

Requirements
-----

(*Italicized items have been coded.*)

**On 2023-06-27, Dave wrote:**

I want to start with the one drive clients subfolder, then move to the internal (not very) shared drive and get a lot of historical clients, and then start into the marketing, which will be proposals as well as client names from Pipedrive.

**On 2023-06-21, Dave wrote:**

The task is to turn our content into triples and integrate it with our structured data.  

At first that sounds overwhelming, but we will bit the elephant a few chunks at a time. 

*First chunk, be able to read a directory and get all the file names, types, dates and sizes. The directory itself will be important later, as we discovered at Morgan, where a document is, is often a good clue as to what it is.*

*So first chunk, write a program (I’m going to suggest python, because chunks 6-10 involve some light weight NLP which will be far easier to do in python, also chunks n-m may involve LLMs or big data or voodoo witchcraft all of which are easier in python).*

*The program should read a directory, and create an instance of gist:Content for each item it finds, and then a triple for the file name, the directory its in, and all the bits of meta data.  We should be able to load it to a Triple store and query it.*

The next several chunks can be done in almost any order, but to give you a hint as to where we are going:

- *Get a fingerprint of the file (so we can detect how many duplicate copies we have)*
- *Recursively do the directory tree, and attach directories to directories*

- Do some simplistic entity resolution for clients and prospects.  This will require some negotiation with Jamie as to how we are going to entity resolve clients and prospects in new SA
- Get some meta data from the files, especially author, but see what else might be interesting.  Usually the tags are worthless and the program used not interesting.  Maybe the original creation date.
- Read some documents with NLP and start experimenting with extracting useful key words.  These will typically be unusual words in English lanaguage and named entities and the like.  This will take an entire career, but just get a start

The objective is to be able to be in new SA system and click on a project and get all the important documents related to that project, or click on a person and get all the documents that person authored, or all the documents that person was named in.  

PS we have about 500K files on the shared folder.  Most are worth indexing.  Some need to be purged as being early drafts on old projects.  Some are sensitive (employee evals and the like)
