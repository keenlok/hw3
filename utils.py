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
    new_pl = []
    for token in line.split(" "):
        docID, weight = token.split(",")
        new_pl.append([docID, float(weight)])

    return new_pl


def convert_file_to_dict(dict_file):
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
    lengths = {}
    with open(length_file, 'r') as f:
        docID_length_arr = f.readline().split(" ")
        for docID_length in docID_length_arr:
            docID, length = docID_length.split(",")
            lengths[docID] = float(length)

    return lengths


def calculate_idf(N_total_docs, doc_freq):
    return math.log(N_total_docs / (doc_freq * 1.0), 10)


def format_result_list(results):
    output = ""
    for i in range(len(results)):
        output += str(results[i])
        if i != len(results) - 1:
            output += " "
    output += "\n"
    return output

# line = "797,1.47712 1069,1.30103 9036,1.60206 9204,1.47712 13089,1.47712"
# print(convert_line_to_posting_list(line))

# dic = convert_file_to_dict("dictionary.txt")
# print(dic)