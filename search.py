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

def run(searcher, analyzer):
    global retrived_scoreDocs, relevant_scoreDocs
    while True:
        print("Hit enter with no input to quit.")
        relevant_command = input("Relevant Query:")
        non_relevant_command = input("NoN Relevant Query:")
        if relevant_command == '' and non_relevant_command =='' :
            return

        if relevant_command:
            print("Searching for relevant documents:", relevant_command)
            relevant_query = QueryParser("contents", analyzer).parse(relevant_command)
            scoreDocs = searcher.search(relevant_query,2500).scoreDocs
            print("%s total relevant documents." % len(scoreDocs))
            relevant_scoreDocs=[]
            for scoreDoc in scoreDocs:
                doc = searcher.doc(scoreDoc.doc)
                relevant_scoreDocs.append( doc.get("name"))
                score=scoreDoc.score
                doc_id=scoreDoc.doc
                print('path:', doc.get("path"), 'name:', doc.get("name"),'score: ',score,'Doc ID :',doc_id)
            # print(relevant_scoreDocs)
            list_relevant = '\n'.join(relevant_scoreDocs)
            # print(list_relevant)
            with open('output.txt','w') as ouput:
                ouput.write(list_relevant)
            with open('output.txt','r') as t ,open('ouutput2.txt','w')as n:
                line = t.readline()
                itr = 1
                while line:
                    n.write( str(str(100) + '\t' + line))
                    line = t.readline()
                    itr+=1
        if non_relevant_command:
            print("Searching for retrived document:", non_relevant_command)
            # line=queries.readline()
            retrived_query = QueryParser("contents", analyzer).parse(non_relevant_command)
            scoreDocs = searcher.search(retrived_query,2500).scoreDocs
            print("%s total retrived documents." % len(scoreDocs))
            retrived_scoreDocs=[]
            for scoreDoc in scoreDocs:
                doc = searcher.doc(scoreDoc.doc)
                retrived_scoreDocs.append(doc.get("name"))
                score=scoreDoc.score
                print('path:', doc.get("path"), 'name:', doc.get("name"),'score: ',score)
            # print(retrived_scoreDocs)

        recall = len(list(set(relevant_scoreDocs).intersection(set(retrived_scoreDocs)))) / float(len(relevant_scoreDocs))
        # print(len(list(set(relevant_scoreDocs).intersection(set(retrived_scoreDocs)))))
        # print(float(len(relevant_scoreDocs)))
        # print(float(len(retrived_scoreDocs)))
        precision = len(list(set(relevant_scoreDocs).intersection(set(retrived_scoreDocs)))) / float(len(retrived_scoreDocs))
        # print(precision)
        # f_measure = (2 * precision * recall) / (precision + recall)
        print('recall: ',recall,'precision: ',precision)

        #impleminting rocchio algorithm

        # wordlist = relevant_command.split()
        # wordfreq = [wordlist.count(w) for w in wordlist] # a list comprehension
        # print(wordfreq)
        # ireader = DirectoryReader.open(directory)
        # filedata = {filename: open(filename, 'r') for filename in relevant_scoreDocs}
        # print(filedata)
        # for doc1 in range(0, len(wordfreq)):
        #     tv = ireader.getTermVector(doc1, "contents")
        #     termsEnum = tv.iterator()
        #
        #     for term in BytesRefIterator.cast_(termsEnum):
        #         dpEnum = termsEnum.postings(None)
        #         dpEnum.nextDoc()  # prime the enum which wothon_modulerks only for the current doc
        #         freq = dpEnum.freq()
            # for f in term:
            #     with open('aaaa.txt','w')as a:
            #         a.write('term:'+str(term.utf8ToString())+'\n'+ '  freq:'+ str(f))
                # print ('term:', term.utf8ToString())
                # print ('  freq:', freq)

        alpha=1
        beta=0.75
        gamma=0.15
        D_relevant=len(list(set(relevant_scoreDocs)))
        # print(D_relevant)
        D_non_relevant=len(list(set(retrived_scoreDocs)))
        # print(D_non_relevant)
        new_vector=[]
        # for term in wordfreq:
        #     new_vector[term] = (wordfreq[term]*alpha)+(beta*1/D_relevant)-(gamma*1/D_non_relevant)
        # print(new_vector)



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
