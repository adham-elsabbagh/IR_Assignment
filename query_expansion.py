import string,sys,os
from os import path
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import search


# BASE_DIR = path.dirname(path.abspath(sys.argv[0]))
# INPUT_DIR = BASE_DIR + "/data/"
# dir = sys.argv[1]
# if len(sys.argv) < 2:
#     print(dir.__doc__)
#     sys.exit(1)
#
# for filename in os.listdir(dir):
#     if not filename.endswith('.xml'):
#         continue
#     with open(os.path.join(dir, filename), 'r') as f:
def query_expanssion(relevant_command):
    global new_line
    synonyms = []

    print("Hit enter with no input to quit.")
    stop_words = set(stopwords.words("english"))
    line = relevant_command
    line = line.replace('\n', '')
    line = line.split(" ", 1)
    new_line = line[0]
    line[1] = line[1].lower()
    line[1] = line[1].translate(str.maketrans('', '', string.punctuation))
    word_tokens = word_tokenize(line[1])
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
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
    # synonyms = []
    print("original query = ",relevant_command)
    print("updated query = ", new_line)
    print("---------------------------------------------------------\n\n")
    return synonyms
    # with open("query_expanded.txt", "w", encoding="utf-8")as fout:
        # 	fout.write(new_line)
        # 	fout.close()
