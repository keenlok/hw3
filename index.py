#!/usr/bin/python3
import math
import re
import nltk
import sys
import getopt
import os
from utils import calculate_weight, length_file, DEBUG, punctuation

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('indexing...')
    indexer = indexing(in_dir, out_dict, out_postings)
    indexer.perform_indexing()

class indexing:

    def __init__(self, in_dir, dictionary, posting):
        self.dict = {}
        self.dir = in_dir
        self.dict_file = dictionary
        self.posting_file = posting
        self.length_file = length_file
        self.dictionary = {}
        self.lengths = {}
        self.all_docID = os.listdir(in_dir)

    def perform_indexing(self):
        loop_count = 0
        lengths = {}
        for filename in sorted(self.all_docID, key=lambda x: int(x)):  # will change back
            count = self.count_doc(os.path.join(self.dir, filename))
            lengths[filename] = self.merge_dic(filename, count)
            print(filename)
            if DEBUG:
                if loop_count == 5:
                    break
                else:
                    loop_count += 1

        self.lengths = lengths
        self.write()

    def count_doc(self, file_path):
        f = open(file_path, 'r')
        tokens = [nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(f.read())]
        tokens = [nltk.PorterStemmer().stem(re.sub(r'[./\-!?^+&%$#()=*:`,"\']', '', word.lower())) for sent in
                  tokens for word in sent if word not in punctuation and not word.isdigit()]

        count = {}
        for token in tokens:
            if token not in count.keys():
                count[token] = 1
            else:
                count[token] += 1

        return count

    def merge_dic(self, docID, dict):
        """
        Merge Dictionaries derived from files into the index.
        """
        length = 0
        for term in dict.keys():
            weight = calculate_weight(dict[term])
            length += pow(weight, 2)
            if term in self.dict.keys():
                self.dict[term].append([docID, weight])
            else:
                self.dict[term] = [[docID, weight]]

        for term in self.dict.keys():
            unsorted = self.dict[term]
            self.dict[term] = sorted(unsorted, key=lambda x: int(x[0]))

        del dict
        # print(self.dict)
        return math.sqrt(length)  # return length of document
    
    def write(self):
        d = open(self.dict_file, 'w')
        p = open(self.posting_file, 'w')

        d.write(str(len(self.all_docID)) + '\n')

        for term in self.dict.keys():
            posting = ["{},{}".format(pair[0], pair[1]) for pair in self.dict[term]]
            p_start = p.tell()
            d.write(term + ' ' + str(len(self.dict[term])) + ' ' + str(p.tell()))
            p.write(' '.join(posting) + '\n')
            d.write(f' {p.tell() - p_start}\n')

        d.close()
        p.close()

        l = open(self.length_file, 'w')
        string_to_write = ''
        for docId in sorted(self.lengths.keys(), key=lambda x: int(x)):
            string_to_write += docId + ',' + str(self.lengths[docId]) + ' '
        string_to_write = string_to_write[:-1]
        l.write(string_to_write)
        l.close()


input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)
