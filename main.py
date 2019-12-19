import sys
import os, threading, time
from os import path, listdir
import nltk
from datetime import datetime
import re
from nltk.tokenize import word_tokenize
import lucene
from os import path, listdir
import numpy
import math
import _pickle as pickle
import parser,index,search,relevance_feedback_1,query_expansion
import string,sys,os


# from java.io import File
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.util import Version
from org.apache.lucene.store import RAMDirectory, SimpleFSDirectory
# Indexer imports:
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
# Retriever imports:
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search.similarities import BM25Similarity,ClassicSimilarity
from java.nio.file import Paths








if __name__ == '__main__':
    dir = sys.argv[1]
    if len(sys.argv) < 2:
        print(dir.__doc__)
        sys.exit(1)
    print('First step is cleaning data...')
    # parser.cleaning_data(dir)

    print('the seconed step is indexing......')
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    start = datetime.now()
    try:
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        INDEX_DIR = "IndexFiles"
        index.IndexFiles(sys.argv[1], os.path.join(base_dir, INDEX_DIR),StandardAnalyzer())
        end = datetime.now()
        print (end - start)
    except Exception as e:
        print ("Failed: ", e)
        raise e

    print('the third step is searching and creating recall and recission values...... ')
    print("Hit enter with no input to quit.")
    relevant_command = input("Relevant Query:")
    non_relevant_command = input("NoN Relevant Query:")

    retrived_scoreDocs, relevant_scoreDocs=[],[]
    directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    searcher.setSimilarity(ClassicSimilarity())
    analyzer = StandardAnalyzer()
    relevant_scoreDocs=search.search_relevant(searcher, analyzer,relevant_command,relevant_scoreDocs)
    retrived_scoreDocs=search.search_non_relevant(searcher, analyzer,non_relevant_command,retrived_scoreDocs)
    print('recall and precision before Rocchio Algorithm','\n')
    search.recall_precision(relevant_scoreDocs,retrived_scoreDocs,)

    print('the fourth step is generating tf-idf...........')
    doc_list = relevance_feedback_1.Doc_processing_module(dir)
    # Documents processing and tf vector and idf vector generation
    doc_node_list = relevance_feedback_1.generate_tf_idf_vectors(doc_list)
    # Query processing and tf vector and idf vector generation
    normal_query = relevance_feedback_1.Query_processing_module(non_relevant_command)
    relevance_feedback_1.generate_tf_idf_vectors_for_query(normal_query)
    # Storing word vocabulary in a file
    with open("vocabulary.p", "wb") as voc_data:
        pickle.dump(relevance_feedback_1.words_database, voc_data)

    # print('the fifth step is creating rocchio algorithm....')
    #
    # with open("vocabulary.p", "rb")as x:
    #     words_database = pickle.load(x,encoding='utf-8')
    #     x.close()
    #
    # with open("doc_data.p", "rb") as y:
    #     tf_idf_node = pickle.load(y,encoding='utf-8')
    #     y.close()
    #
    # with open("doc_id_data.p", "rb") as z:
    #     doc_id = pickle.load(z,encoding='utf-8')
    #     z.close()
    # query_tf_idf = {}
    # lucene_output_docs = {}
    # updated_query_list = []
    # INPUT_DIR = base_dir + "/data/"
    # config = IndexWriterConfig(analyzer)
    # writer = IndexWriter(directory, config)
    #
    #
    # for input_file in listdir(INPUT_DIR):
    #     doc = rocchio_algorithm_new.create_document(input_file)
    #     writer.addDocument(doc)
    # writer.close()
    # # print ("Number of indexed documents: %d\n" % writer.numDocs())
    # # List of docs from lucene search
    # # Queries tf-idf values
    #
    # rocchio_algorithm_new.search_loop(searcher, analyzer)
    # # text processing module for retrieving the text from the documents of the folder
    # query_list = rocchio_algorithm_new.Query_processing_module()
    # query_node_list = rocchio_algorithm_new.generate_tf_idf_vectors_for_query(query_list)
    # print("Query processing and tf-idf over\n")
    # i = 0
    # for query_node in query_node_list:
    #     query_wordlist = relevance_feedback_1.getwordlist(query_node)
    #     query_wordset = set(query_wordlist)
    #     query_tf_idf[i] = {}
    #     query_no = int(query_node.sentence[0:3])
    #     # Calculating tf-idf vector for the query
    #     for word in query_wordset:
    #         if query_node.idf[word] != 100000:
    #             query_tf_idf[i][word] = math.log(1 + query_node.tf[word]) * query_node.idf[word]
    #     b_by_delta_dr = 0.65
    #     # Retrieving only the top 10 documents from lucene output
    #     j = 0
    #     # Implementing Rochio algorithm for each query (query vector updation)
    #     for doc in lucene_output_docs[query_no]:
    #         str_doc = str(doc)
    #         doc_index = doc_id[str_doc]
    #         cur_doc_node = doc_node_list[doc_index]
    #         doc_word_list = relevance_feedback_1.getwordlist(cur_doc_node)
    #         doc_word_set = set(doc_word_list)
    #         # Rochio algorithm for query vector updation
    #         for word in doc_word_set:
    #             if word in query_tf_idf[i]:
    #                 query_tf_idf[i][word] += b_by_delta_dr * math.log(cur_doc_node.tf[word] + 1) * cur_doc_node.idf[
    #                     word]
    #             else:
    #                 query_tf_idf[i][word] = b_by_delta_dr * math.log(cur_doc_node.tf[word] + 1) * cur_doc_node.idf[word]
    #         j += 1
    #         # Only top 10 docs from the retrieved 50 docs
    #         if j == 10:
    #             break
    #     # Sorting the dictionary entries wrt its Values
    #     new_query = str(query_no) + "  "
    #     sorted_dict = sorted(query_tf_idf[i], key=query_tf_idf[i].get, reverse=True)
    #     k = 0
    #     for r in sorted_dict:
    #         new_query += str(r) + " "
    #         k += 1
    #         if k == 10:
    #             break
    #     print("original query = " + query_node.sentence)
    #     print("updated query = " + new_query)
    #     updated_query_list.append(new_query)
    #     print("---------------------------------------------------------\n\n")
    #     i += 1
    # updated_query_scoreDocs=rocchio_algorithm_new.modified_search_loop(searcher, analyzer, updated_query_list)
    # print('recall and precision after Rocchio Algorithm','\n')

    print('the six step is Query Expanssion using word net....... ')
    query_expansion.query_expanssion(non_relevant_command)
    # print(synonyms)
    # print('recall and precision Query Expansion','\n')
    # search.recall_precision(relevant_scoreDocs,synonyms)



    del searcher













    # config = IndexWriterConfig(analyzer)
    # writer = IndexWriter(directory, config)
    # # print ("Number of indexed documents: %d\n" % writer.numDocs())
    # rocchio_algorithm.search_loop(searcher, analyzer, non_relevant_command)
    #
    # for input_file in listdir(INPUT_DIR):  # iterate over all input files
    #     # print "Current file:", input_file
    #     doc = rocchio_algorithm.create_document(input_file)  # call the create_document function
    #     writer.addDocument(doc)  # add the document to the IndexWriter
    # writer.close()
    #
    # # text processing module for retrieving the text from the documents of the folder
    # print(" Lucene output generated...")
    # # query_node_list = relevance_feedback_1.generate_tf_idf_vectors_for_query(normal_query)
    # print("Query processing and tf-idf over\n")
    # updated_normal_query = []
    # i = 0
    # for query_node in query_node_list:
    #     query_wordlist = relevance_feedback_1.getwordlist(query_node)
    #     query_wordset = set(query_wordlist)
    #
    #     query_tf_idf[i] = {}
    #
    #     # Calculating tf-idf vector for the query
    #     for word in query_wordset:
    #
    #         if query_node.idf[word] != 100000:
    #             query_tf_idf[i][word] = math.log(1 + query_node.tf[word]) * query_node.idf[word]
    #     # print('query tf-idf:',query_tf_idf)
    #
    #     b_by_delta_dr = 0.065
    #
    #     # Retrieving only the top 10 documents from lucene output
    #     j = 0
    #
    #     # Implementing Rochio algorithm for each query (query vector updation)
    #     for doc in lucene_output_docs[query_no]:
    #         str_doc = str(doc)
    #         doc_index = doc_id[str_doc]
    #         cur_doc_node = tf_idf_node[doc_index]
    #         doc_word_list = relevance_feedback_1.getwordlist(cur_doc_node)
    #         doc_word_set = set(doc_word_list)
    #
    #         # Rochio algorithm for query vector updation
    #         for word in doc_word_set:
    #
    #             if word in query_tf_idf[i]:
    #
    #                 query_tf_idf[i][word] += b_by_delta_dr * math.log(cur_doc_node.tf[word] + 1) * cur_doc_node.idf[word]
    #             else:
    #                 query_tf_idf[i][word] = b_by_delta_dr * math.log(cur_doc_node.tf[word] + 1) * cur_doc_node.idf[word]
    #         j += 1
    #         # Only top 10 docs from the retrieved 50 docs
    #         if j == 10:
    #             break
    #     # print('query tf-idf:',query_tf_idf)
    #     # End of inner for loop
    #
    #     # Sorting the dictionary entries wrt its Values
    #     new_query =""
    #     sorted_dict = sorted(query_tf_idf[i], key=query_tf_idf[i].get, reverse=True)
    #
    #     k = 0
    #
    #     for r in sorted_dict:
    #
    #         new_query += str(r) + " "
    #
    #         k += 1
    #
    #         if k == 15:
    #             break
    #     print("original query = " + query_node.sentence)
    #     print("updated query = " + new_query)
    #     updated_normal_query.append(new_query)
    #     # print(len(updated_normal_query))
    #     print("---------------------------------------------------------\n\n")
    #     i += 1
    # # End of outer for loop
    # # print('updated normal query legnth',len(updated_normal_query))
    # # finding out the precision, recall for lucene search over the modified queries
    # updated_query_scoreDocs=rocchio_algorithm.modified_search_loop(searcher, analyzer, updated_normal_query)
    #
    # print('updated normal query',updated_query_scoreDocs)
    # print('recall and precision after Rocchio Algorithm','\n')
    # search.recall_precision(relevant_scoreDocs,updated_query_scoreDocs)
    #
    # del searcher







