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
from org.apache.lucene.search.similarities import BM25Similarity,ClassicSimilarity


import lucene


"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def search_relevant (searcher, analyzer,relevant_command,relevant_scoreDocs):
    while True:
        if relevant_command == '':
            return
        if relevant_command:
            print("Searching for relevant documents:", relevant_command)
            relevant_query = QueryParser("contents", analyzer).parse(relevant_command)
            scoreDocs = searcher.search(relevant_query,100).scoreDocs
            print("%s total relevant documents." % len(scoreDocs))
            for scoreDoc in scoreDocs:
                doc = searcher.doc(scoreDoc.doc)
                relevant_scoreDocs.append( doc.get("name"))
                score=scoreDoc.score
                # doc_id=scoreDoc.doc
                print('path:', doc.get("path"), 'name:', doc.get("name"),'score:',score)
            list_relevant = '\n'.join(relevant_scoreDocs)
            with open('output.txt','w') as ouput:
                ouput.write(list_relevant)
            with open('output.txt','r') as t ,open('query_title_document.txt','w')as n:
                line = t.readline()
                itr = 100
                while line:
                    n.write( str(str(100) + '  ' + line))
                    line = t.readline()
                    itr+=1
        return relevant_scoreDocs

def search_non_relevant (searcher, analyzer,non_relevant_command,retrived_scoreDocs):
    while True:
        if non_relevant_command =='':
            return
        if non_relevant_command:
            print("Searching for non relevant document:", non_relevant_command)
            # line=queries.readline()
            retrived_query = QueryParser("contents", analyzer).parse(non_relevant_command)
            scoreDocs = searcher.search(retrived_query,100).scoreDocs
            print("%s total retrived documents." % len(scoreDocs))
            for scoreDoc in scoreDocs:
                doc = searcher.doc(scoreDoc.doc)
                retrived_scoreDocs.append(doc.get("name"))
                score=scoreDoc.score
                print('path:', doc.get("path"), 'name:', doc.get("name"),'score:',score)
        return retrived_scoreDocs

def recall_precision(relevant_scoreDocs,retrived_scoreDocs):

    recall = len(list(set(relevant_scoreDocs).intersection(set(retrived_scoreDocs)))) / float(len(relevant_scoreDocs))
    precision = len(list(set(relevant_scoreDocs).intersection(set(retrived_scoreDocs)))) / float(len(retrived_scoreDocs))
    print('recall:',recall,'  ','precision:',precision)
    print('the length of intersection: ',len(list(set(relevant_scoreDocs).intersection(set(retrived_scoreDocs)))))
    # return relevant_scoreDocs,retrived_scoreDocs

if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    searcher.setSimilarity(BM25Similarity())
    analyzer = StandardAnalyzer()
    # run(searcher, analyzer)
    # recall_precision()
    del searcher
