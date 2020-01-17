# Import the necessay packages
import sys
import os
import nltk
import re
from nltk.tokenize import word_tokenize
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

# ---------------------------- global constants ----------------------------- #

BASE_DIR = path.dirname(path.abspath(sys.argv[0]))
INPUT_DIR = BASE_DIR + "/data_without_titles/"

# Class to store document (node) information
class node_data:

    # A node contains sentence
    def __init__(self, str_sentence):
        self.sentence = str_sentence
        self.tf = {}
        self.idf = {}


# Loading the dictionary from the pickle file
with open("vocabulary.p", "rb")as x:
    words_database = pickle.load(x,encoding='utf-8')

# Loading the dictionary from the pickle file
with open("doc_data.p", "rb") as y:
    doc_node_list = pickle.load(y,encoding='utf-8')

# Loading the dictionary from the doc id hashmap
with open("doc_id_data.p", "rb") as z:
    doc_id = pickle.load(z,encoding='utf-8')

# List of docs from lucene search
lucene_output_docs = {}
# Queries tf-idf values
query_tf_idf = {}


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
print ("Number of indexed documents: %d\n" % writer.numDocs())
for input_file in listdir(INPUT_DIR):  # iterate over all input files
    # print "Current file:", input_file
    doc = create_document(input_file)  # call the create_document function
    writer.addDocument(doc)  # add the document to the IndexWriter
# print "\nNumber of indexed documents =  %d" % writer.numDocs()
writer.close()

# This text processing module is wrt to every query in "query.txt"
def Query_processing_module():
    query_node_list = []
    # file_list = os.listdir("/home/sid/Downloads/Assignement2_IR/Topic"+str(i+1))
    queries = open("query_for_updated_query.txt", 'r')
    i=0
    for query in queries:
        node = node_data(query)
        query_node_list.append(node)
        i+=1
        # print(query_node_list)
    return query_node_list
# End of function

# Get word list from given text from the query.txt
def getwordlist(node):
    sent = node.sentence
    # sent = sent[5:]
    sent = sent.lower()
    sent = re.sub("[^a-zA-Z]+", " ", sent)
    # print sent + "\n"
    sent = sent.strip()
    word_list = sent.split(" ")
    stop_words = nltk.corpus.stopwords.words('english')
    # word_list1 = filter(lambda x: x not in stop_words, word_list)
    # word_list1 = [x for x in word_list if x not in stop_words]
    word_list2 = filter(lambda x: x != '', word_list)
    return word_list2
# end of function

# Module to generate tf-idf vectors corresponding to the sentences
def generate_tf_idf_vectors_for_query(node_list):
    # Calculation of tf
    for node in node_list:
        word_list = getwordlist(node)
        # print word_list
        # print word_list[0] + "in generating tf-idf-vector-forquery"
        # word_list.pop(0)
        word_set = set(word_list)
        for word in word_set:
            node.tf[word] = 0
        # finding out the tf-vector of the node
        for word in word_list:
            node.tf[word] += 1
    # Calculation of idf
    N = len(words_database)
    nodes_to_be_removed = []
    for node in node_list:
        word_list = getwordlist(node)
        word_set = set(word_list)
        for word in word_set:
            if word in words_database:
                ni = words_database[word]
                # print str(ni) + "\n"
                node.idf[word] = math.log(N * 1.0 / ni)
            else:
                node.idf[word] = 100000
    return node_list
# End of function
dict={}
# Function to return lucene search results
def search_loop(searcher, analyzer):

    sum = 0
    with open("query.txt", 'r') as queries:
    # reading every query from the input file
        for command in queries:
            x = word_tokenize(command)
            query_no = float(x[0])
            file_name = str(x[1])
            dict[query_no]=file_name

            print('FILE NAME : '+file_name)
            # print('query number',query_no)
            lucene_output_docs[query_no] = []
            temp_q = command

            com_lenght=command.find('l')+2
            temp_q = temp_q[com_lenght:]

            print ("search loop:  "+ temp_q + "\n")
            query = QueryParser("text", analyzer).parse(temp_q)
            # retrieving top 50 results for each query
            scoreDocs = searcher.search(query, 50).scoreDocs
            # writing output to the file
            with open("lucene_output.txt", "a") as output_file2:
                for scoreDoc in scoreDocs:
                    doc = searcher.doc(scoreDoc.doc)
                    # print doc.get("title")#, 'name:', doc.get("name")
                    temp_str = str(doc.get("title"))
                    lucene_output_docs[query_no].append(temp_str)

                    output_file2.write(str(int(query_no)) + " " + temp_str + "\n")
                # Results retrieved
                output_file2.close()

                print('list of docs',lucene_output_docs[query_no])
                if file_name in lucene_output_docs[query_no]:
                    index = lucene_output_docs[query_no].index(file_name)
                    print('The index of file name is:',index)
                    sum = sum + index
                else:
                    print('not in a list')
                    sum = sum + 50
        average_position = sum / 100
        print('Average postion before rocchio:',average_position)
    # End of outer for loop
    # Closing the queries file
        queries.close()


# End of function
def modified_search_loop(searcher, analyzer, query_list):
    # opening the query file
    # reading every query from the input file
    sum = 0
    print(dict)
    for command in query_list:
        x = word_tokenize(command)
        query_no = int(x[0])
        filename=dict.get(query_no)
        # print(type(filename))
        print('The index of file name is:',filename)
        lucene_output_docs[query_no] = []
        temp_q = command
        temp_q = temp_q[5:]
        # print "search loop:  "+ temp_q + "\n"
        query = QueryParser("text", analyzer).parse(temp_q)
        # retrieving top 50 results for each query
        scoreDocs = searcher.search(query, 50).scoreDocs
        # writing output to the file
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
        # print doc.get("title")#, 'name:', doc.get("name")
            temp_str = str(doc.get("title"))
            lucene_output_docs[query_no].append(temp_str)
            with open("lucene_output_for_updated_queries.txt", "a") as output_file2:
                output_file2.write(str(query_no) + "  " + temp_str + "\n")
        if filename in lucene_output_docs[query_no]:
            index = lucene_output_docs[query_no].index(filename)
            print('The index of updated file name is:',index)
            sum = sum + index
        else:
            print('not in a list')
            sum = sum + 50
    average_position = sum / 100
    print('Average postion after rocchio :',average_position)

# main function
if __name__ == '__main__':

    # Create a searcher for the above defined Directory
    searcher = IndexSearcher(DirectoryReader.open(directory))
    searcher.setSimilarity(ClassicSimilarity())
    # Create a new retrieving analyzer
    analyzer = StandardAnalyzer()
    search_loop(searcher, analyzer)
    # text processing module for retrieving the text from the documents of the folder
    print(" Lucene output generated...")
    # print "Doc processing and tf-idf over"
    query_list = Query_processing_module()
    query_node_list = generate_tf_idf_vectors_for_query(query_list)
    print("Query processing and tf-idf over\n")
    updated_query_list = []
    i = 0
    for query_node in query_node_list:
        query_wordlist = getwordlist(query_node)
        query_wordset = set(query_wordlist)
        query_tf_idf[i] = {}
        query_no = int(query_node.sentence[0:3])
        # Calculating tf-idf vector for the query
        for word in query_wordset:
            if query_node.idf[word] != 100000:
                query_tf_idf[i][word] = math.log(1 + query_node.tf[word]) * query_node.idf[word]
        b_by_delta_dr = 0.65
        # Retrieving only the top 10 documents from lucene output
        j = 0
        # Implementing Rochio algorithm for each query (query vector updation)
        for doc in lucene_output_docs[query_no]:
            str_doc = str(doc)
            doc_index = doc_id[str_doc]
            cur_doc_node = doc_node_list[doc_index]
            doc_word_list = getwordlist(cur_doc_node)
            doc_word_set = set(doc_word_list)
            # Rochio algorithm for query vector updation
            for word in doc_word_set:
                if word in query_tf_idf[i]:
                    query_tf_idf[i][word] += b_by_delta_dr * math.log(cur_doc_node.tf[word] + 1) * cur_doc_node.idf[
                        word]
                else:
                    query_tf_idf[i][word] = b_by_delta_dr * math.log(cur_doc_node.tf[word] + 1) * cur_doc_node.idf[word]
            j += 1
            # Only top 10 docs from the retrieved 50 docs
            if j == 10:
                break
            # print('query tf-idf:', query_tf_idf)
        # Sorting the dictionary entries wrt its Values
        new_query = str(query_no) + "  "
        sorted_dict = sorted(query_tf_idf[i], key=query_tf_idf[i].get, reverse=True)
        k = 0
        for r in sorted_dict:
            new_query += str(r) + " "
            k += 1
            if k == 10:
                break
        print("original query = " + query_node.sentence)
        print("updated query = " + new_query)
        updated_query_list.append(new_query)

        print("---------------------------------------------------------\n\n")
        i += 1
    modified_search_loop(searcher, analyzer, updated_query_list)
