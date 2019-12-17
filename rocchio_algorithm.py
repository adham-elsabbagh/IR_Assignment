# Import the necessay packages
import sys
import os
import lucene
from os import path, listdir
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import RAMDirectory, SimpleFSDirectory
import time
# Indexer imports:
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
# Retriever imports:
from org.apache.lucene.queryparser.classic import QueryParser

# ---------------------------- global constants ----------------------------- #

base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
INPUT_DIR = base_dir + "/data/"

# Class to store document (node) information
class node_data:

    # A node contains sentence
    def __init__(self, str_sentence):
        self.sentence = str_sentence
        self.tf = {}
        self.idf = {}

# # Loading the dictionary from the pickle file
# List of docs from lucene search
itr=0
# Queries tf-idf values
query_tf_idf = {}

def create_document(file_name):
    path = INPUT_DIR + file_name  # assemble the file descriptor
    file = open(path)  # open in read mode
    doc = Document()  # create a new document
    # add the name field
    doc.add(StringField("name", input_file, Field.Store.YES))
    # add the whole book
    doc.add(TextField("contents", file.read(), Field.Store.YES))
    file.close()  # close the file pointer
    return doc

# Initialize lucene and the JVM
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
# Create a new directory. As a SimpleFSDirectory is rather slow ...
directory = RAMDirectory()  # ... we'll use a RAMDirectory!

# Get and configure an IndexWriter
analyzer = StandardAnalyzer()
analyzer = LimitTokenCountAnalyzer(analyzer, 50000000)
config = IndexWriterConfig(analyzer)
writer = IndexWriter(directory, config)
print ("Number of indexed documents: %d\n" % writer.numDocs())
for input_file in listdir(INPUT_DIR):  # iterate over all input files
    # print "Current file:", input_file
    doc = create_document(input_file)  # call the create_document function
    writer.addDocument(doc)  # add the document to the IndexWriter
writer.close()
# End of function
lucene_output_docs = {}
query_no =0
lucene_output_docs[query_no] = []
def search_loop(searcher, analyzer,non_relevant_command):
    # opening the query file
    query = QueryParser("contents", analyzer).parse(non_relevant_command)
    # retrieving top 50 results for each query
    scoreDocs = searcher.search(query, 50).scoreDocs
    non_relevant_scoreDocs=[]
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        non_relevant_scoreDocs.append(str(doc.get("name")))
        lucene_output_docs[query_no].append(non_relevant_scoreDocs)
    list_relevant = '\n'.join(non_relevant_scoreDocs)
    with open("lucene_output_for_normal_query.txt", "a") as output_file2:  #retrieved documents for random query
        output_file2.write(list_relevant + "\n")

# End of function

# making search for the updated query to use the resulted list to calc recall and precission after rocchio
updated_query_scoreDocs=[]
def modified_search_loop(searcher, analyzer, normal_query):
    # reading every query from the input file
    for command in normal_query:
        query = QueryParser("contents", analyzer).parse(command)
        scoreDocs = searcher.search(query, 50).scoreDocs
        # writing output to the file
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            updated_query_scoreDocs.append(str(doc.get("name")))
            lucene_output_docs[query_no].append(updated_query_scoreDocs)
    return updated_query_scoreDocs
# End of function

# End of the recall precision function


