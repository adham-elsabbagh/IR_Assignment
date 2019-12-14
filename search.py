INDEX_DIR = "IndexFiles"

import sys, os, lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.pylucene.search.similarities import PythonClassicSimilarity
from org.apache.lucene.search import \
    BooleanClause, BooleanQuery, Explanation, PhraseQuery, TermQuery
from org.apache.pylucene.search import PythonSimpleCollector
from org.apache.lucene.search.similarities import BM25Similarity,TFIDFSimilarity,ClassicSimilarity

import nltk
import re
from nltk.tokenize import word_tokenize
import lucene
from os import path, listdir
import numpy
import math
"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""

def run(searcher, analyzer):
    global retrived_scoreDocs, relevant_scoreDocs
    while True:
        print("Hit enter with no input to quit.")
        relevant_command = input("Relevant Query:")
        non_relevant_command = input("NoN Relevant Query:")
        if relevant_command == '' and non_relevant_command =='' :
            return

    # with open("newfile.txt", 'r') as queries,open('lucene_output_search_query.txt','w')as q:
    #     line=queries.readline()
        # while line:
        if relevant_command:
            print("Searching for relevant documents:", relevant_command)
            # line=queries.readline()
            query = QueryParser("contents", analyzer).parse(relevant_command)
            Max=100
            scoreDocs = searcher.search(query,Max).scoreDocs
            # print(type(scoreDocs))
            print("%s total relevant documents." % len(scoreDocs))
            relevant_scoreDocs=[]
            for scoreDoc in scoreDocs:
                doc = searcher.doc(scoreDoc.doc)
                relevant_scoreDocs.append( doc.get("name"))
                score=scoreDoc.score
                doc_id=scoreDoc.doc


                print('path:', doc.get("path"), 'name:', doc.get("name"),'score: ',score,'Doc ID :',doc_id)

                # print('content',doc.get('contents'))
                # q.write(str(line+'   '+doc.get("name")))
                # print('content: \n',doc.get('contents'))
        if non_relevant_command:
            print("Searching for retrived document:", non_relevant_command)
            # line=queries.readline()
            query = QueryParser("contents", analyzer).parse(non_relevant_command)
            Max=50
            scoreDocs = searcher.search(query,Max).scoreDocs
            print("%s total retrived documents." % len(scoreDocs))
            retrived_scoreDocs=[]
            for scoreDoc in scoreDocs:
                doc = searcher.doc(scoreDoc.doc)
                retrived_scoreDocs.append(doc.get("name"))
                score=scoreDoc.score
                print('path:', doc.get("path"), 'name:', doc.get("name"),'score: ',score)
                # print('content',doc.get('contents'))
                # q.write(str(line+'   '+doc.get("name")))
                # print('content: \n',doc.get('contents'))
            # print(retrived_scoreDocs)
        recall = len(list(set(relevant_scoreDocs).intersection(set(retrived_scoreDocs)))) / float(len(relevant_scoreDocs))
        print(recall)
        # if len(predicted) != 0:
        precision = len(list(set(relevant_scoreDocs).intersection(set(retrived_scoreDocs)))) / float(len(retrived_scoreDocs))
        print(precision)
        f_measure = (2 * precision * recall) / (precision + recall)
        print('recall: ',recall,'precision: ',precision,'f_measure: ',f_measure)


if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    searcher.setSimilarity(BM25Similarity())
    analyzer = StandardAnalyzer()
    run(searcher, analyzer)
    del searcher
