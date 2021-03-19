import math
import string
import nltk
import re


DEBUG = False
# length_file = "length_old.txt"
length_file = "length.txt"
STEMMER = nltk.PorterStemmer()


def preprocess(str):
    tokens = []
    for word in nltk.word_tokenize(str):
        if all(char in string.punctuation for char in word):
            # print("all punct words found", word)
            continue
        if any(char in string.punctuation for char in word):
            # not normalizing...
            pass
        stemmed = STEMMER.stem(word).lower()
        tokens.append(stemmed)
    return tokens

def free_text_preprocess(str):
    tokens = []
    for word in str.replace('\n', '').split(' '):
        if all(char in string.punctuation for char in word):
            # print("all punct words found", word)
            continue
        if any(char in string.punctuation for char in word):
            # not normalizing...
            pass
        stemmed = STEMMER.stem(word).lower()
        tokens.append(stemmed)
    return tokens


def count_term(tokens):
    count = {}
    for token in tokens:
        if token not in count.keys():
            count[token] = 1
        else:
            count[token] += 1
    return count


def calculate_weight(freq):
    if freq == 0:
        return 0
    weight = 1 + math.log(freq, 10)
    return weight


def convert_line_to_posting_list(line):
    """
    Converts the string form of the posting lists into a proper posting list.
    Returns the converted posting list.
    """
    new_pl = []
    for token in line.split(" "):
        docID, weight = token.split(",")
        new_pl.append([docID, float(weight)])

    return new_pl


def convert_file_to_dict(dict_file):
    """
    Reads the dictionary file and returns the parsed dictionary of terms as well as the
    total number of documents as docNum
    """
    dictionary = {}
    with open(dict_file, 'r') as f:
        docNum = int(f.readline())
        while True:
            line = f.readline()
            if not line:
                break
            term, doc_freq, start, end = line.split(" ")
            dictionary[term] = [int(doc_freq), int(start), int(end)]

    return dictionary, docNum


def convert_file_to_lengths(length_file):
    """
    Reads length file and formats it into a length array to be returned.
    """
    lengths = {}
    with open(length_file, 'r') as f:
        docID_length_arr = f.readline().split(" ")
        for docID_length in docID_length_arr:
            docID, length = docID_length.split(",")
            lengths[docID] = float(length)

    return lengths


def calculate_idf(N_total_docs, doc_freq):
    """
    Calculates idf
    """
    return math.log(N_total_docs / (doc_freq * 1.0), 10)


def format_result_list(results):
    """
    Format search results from list to a space-separated string
    """
    output = ""
    for i in range(len(results)):
        output += str(results[i])
        if i != len(results) - 1:
            output += " "
    output += "\n"
    return output
