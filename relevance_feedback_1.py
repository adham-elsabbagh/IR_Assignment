import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
import os
import numpy
import re
import sys
import math
import pickle
import search


# Class to store document (node) information
class node_data:

    # A node contains sentence
    def __init__(self, str_sentence):
        self.sentence = str_sentence
        self.tf = {}
        self.idf = {}

# vocabulary
words_database = {}
doc_id = {}

# This text processing module is wrt to every doc in the folder "alldocs"
def Doc_processing_module(dir):
    file_node_list = []
    # file_list = os.listdir("/home/sid/Downloads/Assignement2_IR/Topic"+str(i+1))
    file_list = os.listdir(dir)

    temp_tkn = nltk.data.load('tokenizers/punkt/english.pickle')
    i = 0
    # iterate thru every file
    for file in file_list:
        if not file.endswith('.xml'):
            continue
        # print file
        doc_id[file] = i
        # file_ob = open("/home/sid/Downloads/Assignement2_IR/Topic"+str(i+1)+"/"+file,"r")
        file_ob = open(dir+ "/" + file, "r")
        # concatenating all the text in the folder to one entity
        file_text = file_ob.read()
        # final_text = word_by_word_processing(file_text)
        # print (file_text + "\n\n\n")
        node = node_data(file_text)
        file_node_list.append(node)
        i += 1
    with open("doc_id_data.p", "wb") as doc1_data: # store the names of the files in the dir with numbring {'a': 0, 'b': 1, 'c': 2}
        pickle.dump(doc_id, doc1_data)
    return file_node_list
# End of function

# This text processing module is wrt to normal query
def Query_processing_module(non_relevant_command):
    query_node_list = []
    # query = input("Normal Query: ")
    node = node_data(non_relevant_command)
    query_node_list.append(node)
    return query_node_list

# End of function

# Get word list from given text
def getwordlist(node):
    sent = node.sentence
    sent = sent.lower()
    sent = re.sub("[^a-zA-Z]+", " ", sent)
    sent = sent.strip()
    word_list = sent.split(" ")
    stop_words = nltk.corpus.stopwords.words('english')
    word_list2 = filter(lambda x: x != '', word_list)
    return word_list2
# end of function

# Module to generate tf-idf vectors corresponding to the sentences(tf-idf for all the vectors in the all documents)
def generate_tf_idf_vectors(node_list):
    # Dictionary for storing the entire vocabulary
    # Vocabulary stores the no of nodes in which a
    # particular word appears
    # Calculation of tf
    for node in node_list:
        word_list = getwordlist(node)
        word_set = set(word_list)
        for word in word_set:
            node.tf[word] = 0
            if word not in words_database:
                words_database[word] = 1
            else:
                words_database[word] += 1
        # finding out the tf-vector of the node
        for word in word_list:
            node.tf[word] += 1
    # Calculation of idf
    i = 0
    N = len(words_database)
    nodes_to_be_removed = []
    for node in node_list:
        word_list = getwordlist(node)
        word_set = set(word_list)
        if len(word_set) == 0:
            nodes_to_be_removed.append(i)
        for word in word_set:
            ni = words_database[word]
            node.idf[word] = math.log(N * 1.0 / ni)
        i = i + 1
    # end of for loop
    print("size of nodes to be removed =  "+str(len(nodes_to_be_removed)))
    with open("doc_data.p", "wb") as doc_data: #store all tf-idf wordsin dir
        pickle.dump(node_list, doc_data)
    return node_list
# End of function

# Module to generate tf-idf vectors corresponding to the sentences(tf-idf for the normal query)
def generate_tf_idf_vectors_for_query(normal_query):
    # Calculation of tf
    for node in normal_query:
        word_list = getwordlist(node)
        # print str(word_list[0])+" is the indeccs"
        # wordlist.pop(0)
        word_set = set(word_list)
        for word in word_set:
            node.tf[word] = 0
        # finding out the tf-vector of the node
        for word in word_list:
            node.tf[word] += 1
    # Calculation of idf
    N = len(words_database)
    for node in normal_query:
        word_list = getwordlist(node)
        word_set = set(word_list)
        for word in word_set:
            if word in words_database:
                ni = words_database[word]
                # print str(ni) + "\n"
                node.idf[word] = math.log(N * 1.0 / ni)
            else:
                node.idf[word] = 10000
    # print("Size of vocabulary : "+str(len(words_database))+"\n\n")
    return normal_query
# End of function

# main function
if __name__ == '__main__':
    dir = sys.argv[1]
    if len(sys.argv) < 2:
        print(dir.__doc__)
        sys.exit(1)
    # Documents processing and tf vector and idf vector generation
    doc_list = Doc_processing_module(dir)
    doc_node_list = generate_tf_idf_vectors(doc_list)
    # Query processing and tf vector and idf vector generation
    normal_query = Query_processing_module()
    query_node_list = generate_tf_idf_vectors_for_query(normal_query)
    # Storing word vocabulary in a file
    with open("vocabulary.p", "wb") as voc_data: #containing all tf-idf for the normal random query
        pickle.dump(words_database, voc_data)
