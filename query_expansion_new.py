import string,sys,os
from os import path
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import lucene
from os import path, listdir
import math
import _pickle as pickle


# from java.io import File
from org.apache.lucene.search.similarities import BM25Similarity,ClassicSimilarity
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import RAMDirectory, SimpleFSDirectory
import time
# Indexer imports:
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
# from org.apache.lucene.store import SimpleFSDirectory
# Retriever imports:
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser


BASE_DIR = path.dirname(path.abspath(sys.argv[0]))
INPUT_DIR = BASE_DIR + "/data_without_titles/"

def create_document(file_name):
    path = INPUT_DIR + file_name  # assemble the file descriptor
    file = open(path)  # open in read mode
    doc = Document()  # create a new document
    # add the title field
    doc.add(StringField("title", input_file, Field.Store.YES))
    # add the whole book
    doc.add(TextField("text", file.read(), Field.Store.YES))
    file.close()  # close the file pointer
    return doc
lucene_output_docs = {}
# Initialize lucene and the JVM
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
# Create a new directory. As a SimpleFSDirectory is rather slow ...
directory = RAMDirectory()  # ... we'll use a RAMDirectory!
# directory = SimpleFSDirectory()

# Get and configure an IndexWriter
analyzer = StandardAnalyzer()
analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
config = IndexWriterConfig(analyzer)
writer = IndexWriter(directory, config)
for input_file in listdir(INPUT_DIR):  # iterate over all input files
    # print "Current file:", input_file
    doc = create_document(input_file)  # call the create_document function
    writer.addDocument(doc)  # add the document to the IndexWriter
# print "\nNumber of indexed documents =  %d" % writer.numDocs()
writer.close()
searcher = IndexSearcher(DirectoryReader.open(directory))
searcher.setSimilarity(BM25Similarity())

with open("query.txt", 'r') as queries:
# reading every query from the input file
    sum=0
    for command in queries:
        x = word_tokenize(command)
        query_no = float(x[0])
        file_name = str(x[1])

        print('FILE NAME : '+file_name)
        # print('query number',query_no)
        lucene_output_docs[query_no] = []
        temp_q = command

        com_lenght=command.find('l')+2
        temp_q = temp_q[com_lenght:]
        print ("search loop:  "+ temp_q + "\n")

        # f = open("query.txt", "r")
        with open("query_expanded.txt", "w", encoding="utf-8") as fout:
            stop_words = set(stopwords.words("english"))
            line = temp_q
            if not line:
                break
            line = line.replace('\n', '')
            line = line.split(" ", 1)
            new_line = line[0]
            line[1] = line[1].lower()
            line[1] = line[1].translate(str.maketrans('', '', string.punctuation))
            word_tokens = word_tokenize(line[1])
            filtered_sentence = [w for w in word_tokens if not w in stop_words]
            synonyms = []

            count = 0
            for x in filtered_sentence:

                for syn in wordnet.synsets(x):
                    for l in syn.lemmas():
                        if (count < 3):
                            if l.name() not in synonyms:
                                synonyms.append(l.name())
                                count += 1

                count = 0

            synonyms_string = ' '.join(synonyms)
            new_line = " ".join([str(new_line), synonyms_string])
            print('query_expanded:',new_line ,'\n')
            synonyms = []
            fout.write(new_line)
            fout.write('\n')
        fout.close()

        query = QueryParser("text", analyzer).parse(temp_q)
        # retrieving top 50 results for each query
        scoreDocs = searcher.search(query, 10).scoreDocs
        # writing output to the file
        with open("output of query expansion .txt", "a") as output_file2:
            for scoreDoc in scoreDocs:
                doc = searcher.doc(scoreDoc.doc)
                # print doc.get("title")#, 'name:', doc.get("name")
                temp_str = str(doc.get("title"))
                lucene_output_docs[query_no].append(temp_str)

                output_file2.write(str(int(query_no)) + " " + temp_str + "\n")
            # Results retrieved
            output_file2.close()
            # print('FILE NAMEsss : '+file_name)
            print('list of docs',lucene_output_docs[query_no])
            if file_name in lucene_output_docs[query_no]:
                index = lucene_output_docs[query_no].index(file_name)
                print('The index of file name is:',index)
                sum = sum + index
            else:
                print('not in a list')
                sum = sum + 50
    average_position = sum / 100
    print('Average after query expansion:',average_position)
# End of outer for loop
# Closing the queries file
queries.close()

# while True:
#
#     print("Hit enter with no input to quit.")
#     relevant_command = temp_q
#     # f = open("query.txt", "r")
#     fout = open("query_expanded.txt", "w", encoding="utf-8")
#     stop_words = set(stopwords.words("english"))
#     line = relevant_command
#     if not line:
#         break
#     line = line.replace('\n', '')
#     line = line.split(" ", 1)
#     new_line = line[0]
#     line[1] = line[1].lower()
#     line[1] = line[1].translate(str.maketrans('', '', string.punctuation))
#     word_tokens = word_tokenize(line[1])
#     filtered_sentence = [w for w in word_tokens if not w in stop_words]
#
#     synonyms = []
#
#     count = 0
#     for x in filtered_sentence:
#
#         for syn in wordnet.synsets(x):
#             for l in syn.lemmas():
#                 if (count < 3):
#                     if l.name() not in synonyms:
#                         synonyms.append(l.name())
#                         count += 1
#
#         count = 0
#
#     synonyms_string = ' '.join(synonyms)
#     new_line = " ".join([str(new_line), synonyms_string])
#     synonyms = []
#     fout.write(new_line)
#     fout.write('\n')
#
#     # f.close()
#     fout.close()
