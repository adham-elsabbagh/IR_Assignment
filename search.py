INDEX_DIR_with_titles = "IndexFiles_with_titles"
INDEX_DIR_without_titles = "IndexFiles_without_titles"

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
from org.apache.lucene.search.similarities import BM25Similarity,ClassicSimilarity
from org.apache.lucene.util import BytesRef, BytesRefIterator

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
relevant_scoreDocs,retrived_scoreDocs=[],[]
def run(searcher_with_titles,searcher_without_titles, analyzer):
    while True:
        print("Hit enter with no input to quit.")
        file_name = input("file name:")

        relevant_command = input("Query with titles:")
        non_relevant_command = input("Query without titles:")
        if relevant_command == '':
            return

        if relevant_command:
            print("Searching for relevant documents:", relevant_command)
            relevant_query = QueryParser("contents", analyzer).parse(relevant_command)
            scoreDocs = searcher_with_titles.search(relevant_query,10).scoreDocs
            print("%s total relevant documents." % len(scoreDocs))

            for scoreDoc in scoreDocs:
                doc = searcher_with_titles.doc(scoreDoc.doc)
                relevant_scoreDocs.append( doc.get("name"))
                score=scoreDoc.score
                doc_id=scoreDoc.doc
                print('path:', doc.get("path"), 'name:', doc.get("name"),'score: ',score,'Doc ID :',doc_id)
            list_relevant = '\n'.join(relevant_scoreDocs)
            if file_name in relevant_scoreDocs:
                index = relevant_scoreDocs.index(file_name)
                print('The index of file name is:', index)
            else:
                print('not in a list')
            # print(list_relevant)
            with open('output_with_titles.txt','w') as ouput:
                ouput.write(list_relevant)

            # with open('output.txt','r') as t ,open('query_title_document.txt','w')as n:
            #     line = t.readline()
            #     itr = 1
            #     while line:
            #         n.write( str(str(100) + '  ' + line))
            #         line = t.readline()
            #         itr+=1

        if non_relevant_command:
            print("Searching for retrived document without titles:", non_relevant_command)
            # line=queries.readline()
            retrived_query = QueryParser("contents", analyzer).parse(non_relevant_command)
            scoreDocs = searcher_without_titles.search(retrived_query,10).scoreDocs
            print("%s total retrived documents." % len(scoreDocs))

            for scoreDoc in scoreDocs:
                doc = searcher_without_titles.doc(scoreDoc.doc)
                retrived_scoreDocs.append(doc.get("name"))
                score=scoreDoc.score
                doc_id=scoreDoc.doc
                print('path:', doc.get("path"), 'name:', doc.get("name"),'score: ',score,'Doc ID :',doc_id)
            list_retrived = '\n'.join(retrived_scoreDocs)
            if file_name in retrived_scoreDocs:
                index2 = retrived_scoreDocs.index(file_name)
                print('The index of file name is:', index2)
            else:
                print('not in a list')
                # print(list_relevant)
            with open('output_without_titles.txt','w') as ouput:
                ouput.write(list_retrived)


        recall = len(list(set(relevant_scoreDocs).intersection(set(retrived_scoreDocs)))) / float(len(relevant_scoreDocs))
        precision = len(list(set(relevant_scoreDocs).intersection(set(retrived_scoreDocs)))) / float(len(retrived_scoreDocs))
        print('recall:',recall,'  ','precision:',precision)
        print(retrived_scoreDocs)



if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory_with_titles = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR_with_titles)))
    searcher_with_titles = IndexSearcher(DirectoryReader.open(directory_with_titles))
    searcher_with_titles.setSimilarity(BM25Similarity())

    directory_without_titles = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR_without_titles)))
    searcher_without_titles = IndexSearcher(DirectoryReader.open(directory_without_titles))
    searcher_without_titles.setSimilarity(BM25Similarity())

    analyzer = StandardAnalyzer()
    run(searcher_with_titles,searcher_without_titles, analyzer)
    del searcher_with_titles,searcher_without_titles
