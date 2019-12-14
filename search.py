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


"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
# class SimpleSimilarity(PythonClassicSimilarity):
#
#     def lengthNorm(self, numTerms):
#         return 1.0
#
#     def tf(self, freq):
#         return freq
#
#     def sloppyFreq(self, distance):
#         return 2.0
#
#     def idf(self, docFreq, numDocs):
#         return 1.0
#
#     def idfExplain(self, collectionStats, termStats):
#
#         return Explanation.match(1.0, "inexplicable", [])


def run(searcher, analyzer):
    while True:
        print("Hit enter with no input to quit.")
        command = input("Query:")
        if command == '':
            return
    # with open("newfile.txt", 'r') as queries,open('lucene_output_search_query.txt','w')as q:
    #     line=queries.readline()
        # while line:
        print("Searching for:", command)
        # line=queries.readline()
        query = QueryParser("contents", analyzer).parse(command)
        # searcher.setSimilarity(SimpleSimilarity)
        scoreDocs = searcher.search(query,50).scoreDocs
        print("%s total matching documents." % len(scoreDocs))

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print('path:', doc.get("path"), 'name:', doc.get("name"))
            print (scoreDoc.toString())
            # print('content',doc.get('contents'))
            # q.write(str(line+'   '+doc.get("name")))
            # print('content: \n',doc.get('contents'))

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
